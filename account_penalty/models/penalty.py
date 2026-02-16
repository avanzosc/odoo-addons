# Copyright 2025 Aner Arregi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class Penalty(models.Model):
    _name = "account.penalty"
    _description = "Penalty"

    name = fields.Char(required=True)
    quantity = fields.Float(required=True)
    amount = fields.Monetary(required=True)
    invoice_date = fields.Date(required=True)
    to_invoice = fields.Boolean(default=True)
    invoice_id = fields.Many2one("account.move", string="Invoice")
    partner_id = fields.Many2one("res.partner", required=True)
    journal_id = fields.Many2one(
        "account.journal", required=True, domain="[('type', '=', 'sale')]"
    )
    penalty_type_id = fields.Many2one("penalty.type", required=True)
    product_id = fields.Many2one(
        related="penalty_type_id.product_id", string="Product", readonly=True
    )
    currency_id = fields.Many2one("res.currency", related="journal_id.currency_id")
    state = fields.Selection(
        [("draft", "To Invoice"), ("invoiced", "Invoiced")],
        string="Status",
        default="draft",
        compute="_compute_state",
        store=True,
    )

    @api.depends("to_invoice", "invoice_id")
    def _compute_state(self):
        for penalty in self:
            penalty.state = "invoiced" if penalty.invoice_id else "draft"

    def action_create_invoice(self):
        penalties_to_invoice = self.filtered(
            lambda p: p.to_invoice and not p.invoice_id
        )

        if not penalties_to_invoice:
            if self:
                raise UserError(
                    _(
                        """No selectable penalties to invoice.
                                  Please select penalties with status "To Invoice"."""
                    )
                )
            else:
                raise UserError(_("No penalties to invoice."))

        invoices_created = self.env["account.move"]
        grouped_penalties = {}

        for penalty in penalties_to_invoice:
            key = (penalty.partner_id.id, penalty.journal_id.id)
            if key not in grouped_penalties:
                grouped_penalties[key] = []
            grouped_penalties[key].append(penalty)

        for (partner_id, journal_id), penalties in grouped_penalties.items():
            invoice_lines = []
            for penalty in penalties:
                invoice_lines.append(
                    (
                        0,
                        0,
                        {
                            "product_id": penalty.penalty_type_id.product_id.id,
                            "name": penalty.name,
                            "quantity": penalty.quantity,
                            "price_unit": penalty.amount,
                        },
                    )
                )

            max_date = max(penalty.invoice_date for penalty in penalties)

            invoice = self.env["account.move"].create(
                {
                    "partner_id": partner_id,
                    "journal_id": journal_id,
                    "move_type": "out_invoice",
                    "invoice_date": max_date,
                    "invoice_line_ids": invoice_lines,
                }
            )

            invoices_created |= invoice

            for penalty in penalties:
                penalty.write(
                    {
                        "invoice_id": invoice.id,
                        "to_invoice": False,
                    }
                )

        if invoices_created:
            action = {
                "type": "ir.actions.act_window",
                "res_model": "account.move",
                "view_mode": "tree,form",
                "target": "current",
            }
            if len(invoices_created) == 1:
                action.update(
                    {
                        "res_id": invoices_created.id,
                        "view_mode": "form",
                    }
                )
            else:
                action.update(
                    {
                        "domain": [("id", "in", invoices_created.ids)],
                        "name": _("Created Invoices"),
                    }
                )
            return action
