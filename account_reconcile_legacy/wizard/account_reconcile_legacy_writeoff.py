# Copyright 2026 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from odoo import Command, _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools import float_is_zero


class AccountReconcileLegacyWriteoff(models.TransientModel):
    _name = "account.reconcile.legacy.writeoff"
    _description = "Descuadre conciliación manual clásica"
    _inherit = "analytic.mixin"

    line_ids = fields.Many2many(
        comodel_name="account.move.line",
        string="Apuntes",
        readonly=True,
    )

    company_id = fields.Many2one(
        comodel_name="res.company",
        required=True,
        readonly=True,
    )

    currency_id = fields.Many2one(
        related="company_id.currency_id",
        readonly=True,
    )

    source_account_id = fields.Many2one(
        comodel_name="account.account",
        string="Cuenta a conciliar",
        readonly=True,
    )

    partner_id = fields.Many2one(
        comodel_name="res.partner",
        readonly=True,
    )

    account_id = fields.Many2one(
        comodel_name="account.account",
        string="Cuenta",
        check_company=True,
    )

    journal_id = fields.Many2one(
        comodel_name="account.journal",
        string="Diario",
        required=True,
        check_company=True,
    )

    label = fields.Char(
        string="Etiqueta",
        default="Descuadre",
        required=True,
    )

    balance = fields.Monetary(
        string="Saldo",
        currency_field="currency_id",
        readonly=True,
    )

    amount = fields.Monetary(
        string="Importe",
        currency_field="currency_id",
        readonly=True,
    )

    date = fields.Date(
        string="Fecha de descuadre",
        required=True,
        default=fields.Date.context_today,
    )

    @api.model
    def create_from_lines(self, line_ids):
        lines = self.env["account.move.line"].browse(line_ids).exists()

        if not lines:
            raise UserError(_("No hay apuntes seleccionados."))

        companies = lines.mapped("company_id")
        if len(companies) != 1:
            raise UserError(_("Los apuntes deben pertenecer a la misma compañía."))

        accounts = lines.mapped("account_id")
        if len(accounts) != 1:
            raise UserError(_("Los apuntes deben pertenecer a la misma cuenta."))

        company = companies
        source_account = accounts

        balance = sum(lines.mapped("amount_residual"))

        if float_is_zero(
            balance,
            precision_rounding=company.currency_id.rounding,
        ):
            raise UserError(_("Los apuntes seleccionados ya están cuadrados."))

        first_partner = lines[0].partner_id
        same_partner = all(line.partner_id == first_partner for line in lines)

        journal = self.env["account.journal"].search(
            [
                ("company_id", "=", company.id),
                ("type", "=", "general"),
            ],
            limit=1,
        )

        if not journal:
            raise UserError(
                _("No existe un diario de tipo Miscelánea para esta compañía.")
            )

        wizard = self.create(
            {
                "line_ids": [Command.set(lines.ids)],
                "company_id": company.id,
                "source_account_id": source_account.id,
                "partner_id": (
                    first_partner.id if same_partner and first_partner else False
                ),
                "journal_id": journal.id,
                "balance": balance,
                "amount": abs(balance),
                "date": fields.Date.context_today(self),
            }
        )

        return {
            "wizard_id": wizard.id,
            "view_id": self.env.ref(
                "account_reconcile_legacy.view_account_reconcile_legacy_writeoff_form"
            ).id,
        }

    def action_apply(self):
        self.ensure_one()

        lines = self.line_ids.exists()

        if not lines:
            raise UserError(_("Los apuntes ya no existen."))

        if not self.account_id:
            raise UserError(_("Debe indicar una cuenta."))

        balance = sum(lines.mapped("amount_residual"))

        currency = self.company_id.currency_id

        if float_is_zero(
            balance,
            precision_rounding=currency.rounding,
        ):
            raise UserError(_("Los apuntes seleccionados ya están cuadrados."))

        source_account = self.source_account_id

        if self.account_id == source_account:
            raise UserError(
                _(
                    "La cuenta de descuadre debe ser diferente "
                    "de la cuenta que se está conciliando."
                )
            )

        source_debit = max(-balance, 0.0)
        source_credit = max(balance, 0.0)

        writeoff_debit = max(balance, 0.0)
        writeoff_credit = max(-balance, 0.0)

        move = self.env["account.move"].create(
            {
                "move_type": "entry",
                "company_id": self.company_id.id,
                "journal_id": self.journal_id.id,
                "date": self.date,
                "ref": self.label,
                "line_ids": [
                    Command.create(
                        {
                            "name": self.label,
                            "account_id": source_account.id,
                            "partner_id": self.partner_id.id or False,
                            "debit": source_debit,
                            "credit": source_credit,
                        }
                    ),
                    Command.create(
                        {
                            "name": self.label,
                            "account_id": self.account_id.id,
                            "debit": writeoff_debit,
                            "credit": writeoff_credit,
                            "analytic_distribution": self.analytic_distribution,
                        }
                    ),
                ],
            }
        )

        move.action_post()

        reconciliation_line = move.line_ids.filtered(
            lambda line: line.account_id == source_account
        )

        if len(reconciliation_line) != 1:
            raise UserError(_("No se ha podido localizar la línea de descuadre."))

        (lines + reconciliation_line).reconcile()

        return {
            "type": "ir.actions.client",
            "tag": "reload",
        }
