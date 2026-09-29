# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import Command, _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval

from odoo.addons.base_import_wizard.models.base_import import check_number, convert2str


class AccountMoveImport(models.Model):
    _name = "account.move.import"
    _inherit = "base.import"
    _description = "Wizard to import account moves"

    def default_journal_id(self):
        default_dict = self.env["account.move"].default_get(["journal_id"])
        return default_dict.get("journal_id")

    def default_accounting_date(self):
        default_dict = self.env["account.move"].default_get(["date"])
        return default_dict.get("date")

    import_line_ids = fields.One2many(
        comodel_name="account.move.import.line",
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        index=True,
        required=True,
        default=lambda self: self.env.company.id,
    )
    account_move_id = fields.Many2one(
        string="Account Move",
        comodel_name="account.move",
    )
    ref = fields.Char(
        string="Account Move Ref",
    )
    accounting_date = fields.Date(
        required=True,
        default=default_accounting_date,
    )
    journal_id = fields.Many2one(
        string="Journal",
        comodel_name="account.journal",
        required=True,
        default=default_journal_id,
    )
    search_partner_by_ref = fields.Boolean(
        string="Search Partner Only By Ref",
        default=False,
    )

    @api.depends(
        "import_line_ids",
        "import_line_ids.state",
        "import_line_ids.debit",
        "import_line_ids.credit",
    )
    def _compute_state(self):
        result = super()._compute_state()

        for record in self:
            if record.state == "pass" and not record._is_balanced():
                record.state = "error"
        return result

    def _get_line_values(self, row_values, datemode=False):
        self.ensure_one()
        values = super()._get_line_values(row_values, datemode=datemode)
        if row_values:
            account_code = row_values.get("Account", "")
            name = row_values.get("Name", "")
            debit = row_values.get("Debit", 0.0)
            credit = row_values.get("Credit", 0.0)
            partner_ref = row_values.get("Partner Code", "")
            partner_name = row_values.get("Partner Name", "")
            log_info = ""
            if account_code:
                values.update(
                    {
                        "account_code": convert2str(account_code),
                        "name": convert2str(name),
                        "debit": check_number(debit),
                        "credit": check_number(credit),
                        "partner_ref": convert2str(partner_ref),
                        "partner_name": convert2str(partner_name),
                        "log_info": log_info,
                    }
                )
        return values

    @api.depends(
        "import_line_ids",
        "import_line_ids.log_info",
        "import_line_ids.debit",
        "import_line_ids.credit",
        "import_line_ids.state",
    )
    def _compute_log_info(self):
        result = super()._compute_log_info()

        for record in self:
            if (
                record.import_line_ids
                and all(
                    line.state in ("pass", "done") for line in record.import_line_ids
                )
                and not record._is_balanced()
            ):
                total_debit, total_credit = record._get_balance_totals()

                balance_log = _(
                    "Error: The journal entry is not balanced.\n"
                    "Total Debit: %(debit)s\n"
                    "Total Credit: %(credit)s"
                ) % {
                    "debit": total_debit,
                    "credit": total_credit,
                }

                record.log_info = (
                    f"{record.log_info}\n{balance_log}"
                    if record.log_info
                    else balance_log
                )
        return result

    def _create_account_move(self):
        self.ensure_one()
        total_debit, total_credit = self._get_balance_totals()
        if not self.company_id.currency_id.is_zero(total_debit - total_credit):
            raise ValidationError(
                _(
                    "The journal entry cannot be created because "
                    "it is not balanced.\n"
                    "Total Debit: %(debit)s\n"
                    "Total Credit: %(credit)s"
                )
                % {
                    "debit": total_debit,
                    "credit": total_credit,
                }
            )
        lines = self.import_line_ids.filtered(
            lambda line: line.action == "create" and line.state == "pass"
        )
        if not lines:
            raise ValidationError(_("There are no valid lines to create."))
        line_commands = []
        for line in lines:
            line_commands.append(Command.create(line._account_move_line_vals()))
        vals = self._account_move_vals()
        vals["line_ids"] = line_commands
        return self.env["account.move"].create(vals)

    def _account_move_vals(self):
        self.ensure_one()

        return {
            "move_type": "entry",
            "journal_id": self.journal_id.id,
            "date": self.accounting_date,
            "ref": self.ref or False,
        }

    def _get_balance_totals(self):
        self.ensure_one()

        total_debit = sum(self.import_line_ids.mapped("debit"))
        total_credit = sum(self.import_line_ids.mapped("credit"))

        return total_debit, total_credit

    def _is_balanced(self):
        self.ensure_one()

        total_debit, total_credit = self._get_balance_totals()

        return self.company_id.currency_id.is_zero(total_debit - total_credit)

    def button_open_account_move(self):
        self.ensure_one()
        action = self.env.ref("account.action_move_line_form")
        action_dict = action.read()[0] if action else {}
        domain = expression.AND(
            [[("id", "=", self.account_move_id.id)], safe_eval(action.domain or "[]")]
        )
        action_dict.update({"domain": domain})
        return action_dict


class AccountMoveImportLine(models.Model):
    _name = "account.move.import.line"
    _inherit = "base.import.line"
    _description = "Lines to import account moves"

    import_id = fields.Many2one(
        comodel_name="account.move.import",
        copy=False,
    )
    action = fields.Selection(
        selection_add=[
            ("create", "Create"),
        ],
        ondelete={"create": "set default"},
    )
    account_move_id = fields.Many2one(
        comodel_name="account.move",
        related="import_id.account_move_id",
        store=True,
    )
    account_code = fields.Char(
        states={"done": [("readonly", True)]},
        copy=False,
        required=True,
    )
    name = fields.Char(
        states={"done": [("readonly", True)]},
        copy=False,
    )
    debit = fields.Float(
        states={"done": [("readonly", True)]},
        copy=False,
    )
    credit = fields.Float(
        states={"done": [("readonly", True)]},
        copy=False,
    )
    partner_ref = fields.Char(
        states={"done": [("readonly", True)]},
        copy=False,
    )
    partner_name = fields.Char(
        states={"done": [("readonly", True)]},
        copy=False,
    )
    account_id = fields.Many2one(
        comodel_name="account.account",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        states={"done": [("readonly", True)]},
        copy=False,
    )

    def _action_validate(self):
        update_values = super()._action_validate()
        log_infos = []
        account = partner = False
        if self.account_code:
            account, log_info_account = self._check_account()
            if log_info_account:
                log_infos.append(log_info_account)
        if self.partner_ref or self.partner_name:
            partner, log_info_partner = self._check_partner()
            if log_info_partner:
                log_infos.append(log_info_partner)
        if self.debit < 0 or self.credit < 0:
            log_infos.append(_("Debit and credit cannot be negative."))
        if self.debit and self.credit:
            log_infos.append(_("A line cannot have both debit and credit."))
        if not self.debit and not self.credit:
            log_infos.append(_("Debit or credit must have an amount."))
        state = "error" if log_infos else "pass"
        action = "create" if state != "error" else "nothing"
        update_values.update(
            {
                "account_id": account and account.id,
                "partner_id": partner and partner.id,
                "log_info": "\n".join(log_infos),
                "state": state,
                "action": action,
            }
        )
        return update_values

    def _action_process(self):
        update_values = super()._action_process()

        if self.action == "create" and self.state != "done":
            account_move = self.import_id.account_move_id

            if not account_move:
                account_move = self.import_id._create_account_move()
                self.import_id.account_move_id = account_move

            update_values.update(
                {
                    "state": "done",
                }
            )

        return update_values

    def _check_account(self):
        self.ensure_one()
        log_info = ""
        if self.account_id:
            return self.account_id, log_info
        account_obj = self.env["account.account"]
        search_domain = [("code", "=", self.account_code)]
        if self.import_id.company_id:
            search_domain = expression.AND(
                [
                    [
                        ("company_ids", "in", [self.import_id.company_id.id]),
                    ],
                    search_domain,
                ]
            )
            account_obj = account_obj.with_company(self.import_id.company_id)
        accounts = account_obj.search(search_domain)
        if not accounts:
            accounts = False
            log_info = _("Error: No account found.")
        elif len(accounts) > 1:
            accounts = False
            log_info = _("Error: More than one account found.")
        return accounts and accounts[:1], log_info

    def _check_partner(self):
        self.ensure_one()
        log_info = ""
        if self.partner_id:
            return self.partner_id, log_info
        partner_obj = self.env["res.partner"]
        search_domain = [("name", "=", self.partner_name)]
        if self.partner_ref:
            search_domain = expression.AND(
                [[("ref", "=", self.partner_ref)], search_domain]
            )
            if self.import_id.search_partner_by_ref:
                search_domain = [("ref", "=", self.partner_ref)]
        if self.import_id.company_id:
            search_domain = expression.AND(
                [
                    [
                        "|",
                        ("company_id", "=", self.import_id.company_id.id),
                        ("company_id", "=", False),
                    ],
                    search_domain,
                ]
            )
            partner_obj = partner_obj.with_company(self.import_id.company_id)
        partners = partner_obj.search(search_domain)
        if not partners:
            partners = False
            log_info = _("Error: No partner found.")
        elif len(partners) > 1:
            partners = False
            log_info = _("Error: More than one partner found.")
        return partners and partners[:1], log_info

    def _account_move_line_vals(self):
        self.ensure_one()

        return {
            "account_id": self.account_id.id,
            "partner_id": self.partner_id.id if self.partner_id else False,
            "name": self.name,
            "debit": self.debit,
            "credit": self.credit,
        }
