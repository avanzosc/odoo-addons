# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval

from odoo.addons.base_import_wizard.models.base_import import convert2str


class ResPartnerPaymentImport(models.Model):
    _name = "res.partner.payment.import"
    _inherit = "base.import"
    _description = "Wizard to import contact payment mode"

    import_line_ids = fields.One2many(
        comodel_name="res.partner.payment.import.line",
    )
    res_partner_count = fields.Integer(
        string="# Contacts",
        compute="_compute_res_partner_count",
    )

    def _get_line_values(self, row_values=False):
        self.ensure_one()
        values = super()._get_line_values(row_values=row_values)
        if row_values:
            contact_name = row_values.get("Name", "")
            contact_code = row_values.get("Code", "")
            contact_payment_mode = row_values.get("PaymentMode", "")
            contact_payment_term = row_values.get("PaymentTerm", "")
            contact_account_fiscal_position = row_values.get(
                "AccountFiscalPosition", ""
            )
            log_info = ""
            if not contact_name and not contact_code:
                return {}
            values.update(
                {
                    "contact_name": contact_name.title(),
                    "contact_code": convert2str(contact_code),
                    "contact_payment_mode": convert2str(contact_payment_mode),
                    "contact_payment_term": convert2str(contact_payment_term),
                    "contact_account_fiscal_position": convert2str(
                        contact_account_fiscal_position
                    ),
                    "log_info": log_info,
                }
            )
        return values

    def _compute_res_partner_count(self):
        for record in self:
            record.res_partner_count = len(record.mapped("import_line_ids.contact_id"))

    def button_open_res_partner(self):
        self.ensure_one()
        contacts = self.mapped("import_line_ids.contact_id")
        action = self.env.ref("contacts.action_contacts")
        action_dict = action.read()[0] if action else {}
        domain = expression.AND(
            [[("id", "in", contacts.ids)], safe_eval(action.domain or "[]")]
        )
        action_dict.update({"domain": domain})
        return action_dict


class ResPartnerPaymentImportLine(models.Model):
    _name = "res.partner.payment.import.line"
    _inherit = "base.import.line"
    _description = "Lines to import contacts payment mode"

    @api.model
    def _get_selection_contact_type(self):
        return self.env["res.partner"].fields_get(allfields=["type"])["type"][
            "selection"
        ]

    def default_contact_type(self):
        default_dict = self.env["res.partner"].default_get(["type"])
        return default_dict.get("type")

    import_id = fields.Many2one(
        comodel_name="res.partner.payment.import",
    )
    action = fields.Selection(
        selection=[
            ("update", "Update"),
            ("nothing", "Nothing"),
        ],
        default="nothing",
        states={"done": [("readonly", True)]},
        copy=False,
        required=True,
    )
    contact_id = fields.Many2one(string="Contact", comodel_name="res.partner")
    contact_name = fields.Char(
        states={"done": [("readonly", True)]},
        copy=False,
    )
    contact_code = fields.Char(
        states={"done": [("readonly", True)]},
        copy=False,
    )
    contact_payment_mode = fields.Char(
        string="Payment Mode Name",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    contact_payment_term = fields.Char(
        string="Payment Term Name",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    contact_account_fiscal_position = fields.Char(
        string="Account Fiscal Position Name",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    payment_mode_id = fields.Many2one(
        string="Payment Mode",
        comodel_name="account.payment.mode",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    payment_term_id = fields.Many2one(
        string="Payment Term",
        comodel_name="account.payment.term",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    account_fiscal_position_id = fields.Many2one(
        string="Account Fiscal Position",
        comodel_name="account.fiscal.position",
        states={"done": [("readonly", True)]},
        copy=False,
    )

    def action_validate(self):
        super().action_validate()
        line_values = []
        for line in self.filtered(lambda ln: ln.state != "done"):
            log_info = ""
            contact = payment_mode = payment_term = fiscal_position = False
            if line.contact_name or line.contact_code:
                contact, log_info_contact = line._check_contact()
                if log_info_contact:
                    log_info += log_info_contact
            if line.contact_payment_mode:
                payment_mode, log_info_payment_mode = line._check_payment_mode()
                if log_info_payment_mode:
                    log_info += log_info_payment_mode
            if line.contact_payment_term:
                payment_term, log_info_payment_term = line._check_payment_term()
                if log_info_payment_term:
                    log_info += log_info_payment_term
            if line.contact_account_fiscal_position:
                fiscal_position, log_info_fiscal_position = line._check_fiscal_position(
                    contact=contact
                )
                if log_info_fiscal_position:
                    log_info += log_info_fiscal_position
            state = "error" if log_info else "pass"
            action = "nothing"
            if state != "error":
                action = "update"
            update_values = {
                "contact_id": contact and contact.id,
                "payment_mode_id": payment_mode and payment_mode.id,
                "payment_term_id": payment_term and payment_term.id,
                "account_fiscal_position_id": fiscal_position and fiscal_position.id,
                "log_info": log_info,
                "state": state,
                "action": action,
            }
            line_values.append(
                (
                    1,
                    line.id,
                    update_values,
                )
            )
        return line_values

    def action_process(self):
        super().action_validate()
        line_values = []
        for line in self.filtered(lambda ln: ln.state not in ("error", "done")):
            if line.action == "update":
                contact, log_info = line._check_contact()
                if contact and line.payment_mode_id:
                    contact.customer_payment_mode_id = line.payment_mode_id.id
                if contact and line.payment_term_id:
                    contact.property_payment_term_id = line.payment_term_id.id
                if contact and line.account_fiscal_position_id:
                    contact.property_account_position_id = (
                        line.account_fiscal_position_id.id
                    )
            else:
                continue
            state = "error" if log_info else "done"
            line.write({"contact_id": contact.id, "log_info": log_info, "state": state})
            line_values.append(
                (
                    1,
                    line.id,
                    {
                        "contact_id": contact.id,
                        "log_info": log_info,
                        "state": state,
                    },
                )
            )
        return line_values

    def _check_contact(self):
        self.ensure_one()
        log_info = ""
        if self.contact_id:
            return self.contact_id, log_info
        contact_obj = self.env["res.partner"]
        if self.contact_code:
            search_domain = [("ref", "=", self.contact_code)]
        else:
            search_domain = [("name", "=", self.contact_name)]
        contacts = contact_obj.search(search_domain)
        if not contacts:
            contacts = False
            log_info = _("Error: No contact found.")
        elif len(contacts) > 1:
            contacts = False
            log_info = _("Error: More than one contact found.")
        return contacts and contacts[:1], log_info

    def _check_payment_mode(self):
        self.ensure_one()
        log_info = ""
        if self.payment_mode_id:
            return self.payment_mode_id, log_info
        payment_mode_obj = self.env["account.payment.mode"]
        if self.contact_payment_mode:
            search_domain = [
                ("name", "=", self.contact_payment_mode),
                ("payment_type", "=", "inbound"),
            ]
            payment_modes = payment_mode_obj.search(search_domain)
            if not payment_modes:
                payment_modes = False
                log_info = _("Error: No payment mode found.")
            elif len(payment_modes) > 1:
                payment_modes = False
                log_info = _("Error: More than one payment modes found.")
        return payment_modes and payment_modes[:1], log_info

    def _check_payment_term(self):
        self.ensure_one()
        log_info = ""
        if self.payment_term_id:
            return self.payment_term_id, log_info
        payment_term_obj = self.env["account.payment.term"]
        if self.contact_payment_term:
            search_domain = [("name", "=", self.contact_payment_term)]
            payment_terms = payment_term_obj.search(search_domain)
            if not payment_terms:
                payment_terms = False
                log_info = _("Error: No payment term found.")
            elif len(payment_terms) > 1:
                payment_terms = False
                log_info = _("Error: More than one payment terms found.")
        return payment_terms and payment_terms[:1], log_info

    def _check_fiscal_position(self, contact=False):
        self.ensure_one()
        log_info = ""
        if self.account_fiscal_position_id:
            return self.account_fiscal_position_id, log_info
        fiscal_position_obj = self.env["account.fiscal.position"]
        if self.contact_account_fiscal_position:
            search_domain = [("name", "=", self.contact_account_fiscal_position)]
            if contact and contact.company_id:
                search_domain = expression.AND(
                    [[("company_id", "=", contact.company_id.id)], search_domain]
                )
            fiscal_positions = fiscal_position_obj.search(search_domain)
            if not fiscal_positions:
                fiscal_positions = False
                log_info = _("Error: No fiscal position found.")
            elif len(fiscal_positions) > 1:
                fiscal_positions = False
                log_info = _("Error: More than one fiscal position found.")
        return fiscal_positions and fiscal_positions[:1], log_info
