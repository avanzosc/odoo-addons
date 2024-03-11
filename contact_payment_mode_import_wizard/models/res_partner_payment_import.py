# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, fields, models
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
    partner_count = fields.Integer(
        string="# Contacts",
        compute="_compute_partner_count",
    )
    import_type = fields.Selection(
        string="Sale/Purchase",
        selection=[("sale", "Sale"), ("purchase", "Purchase"), ("both", "Both")],
        states={"done": [("readonly", True)]},
        copy=False,
        required=True,
        default="both",
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        index=True,
        required=True,
        default=lambda self: self.env.company.id,
    )

    def _get_line_values(self, row_values, datemode=False):
        self.ensure_one()
        values = super()._get_line_values(row_values, datemode=datemode)
        if row_values:
            contact_name = row_values.get("Name", "")
            contact_code = row_values.get("Code", "")
            contact_payment_mode = row_values.get("PaymentMode", "")
            contact_payment_term = row_values.get("PaymentTerm", "")
            contact_account_fiscal_position = row_values.get(
                "AccountFiscalPosition", ""
            )
            log_info = ""
            if contact_name or contact_code:
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

    def _compute_partner_count(self):
        for record in self:
            record.partner_count = len(record.mapped("import_line_ids.contact_id"))

    def button_open_partner(self):
        self.ensure_one()
        contacts = self.mapped("import_line_ids.contact_id")
        action = self.env["ir.actions.actions"]._for_xml_id("contacts.action_contacts")
        action["domain"] = expression.AND(
            [[("id", "in", contacts.ids)], safe_eval(action.get("domain") or "[]")]
        )
        action["context"] = dict(self._context, create=False)
        return action


class ResPartnerPaymentImportLine(models.Model):
    _name = "res.partner.payment.import.line"
    _inherit = "base.import.line"
    _description = "Lines to import contacts payment mode"

    import_id = fields.Many2one(
        comodel_name="res.partner.payment.import",
    )
    action = fields.Selection(
        selection_add=[
            ("update", "Update"),
        ],
        ondelete={"update": "set default"},
    )
    contact_id = fields.Many2one(
        string="Contact",
        comodel_name="res.partner",
    )
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

    def _action_validate(self):
        update_values = super()._action_validate()
        log_infos = []
        contact = payment_mode = payment_term = fiscal_position = False
        if self.contact_name or self.contact_code:
            contact, log_info_contact = self._check_contact()
            if log_info_contact:
                log_infos.append(log_info_contact)
        if self.contact_payment_mode:
            payment_mode, log_info_payment_mode = self._check_payment_mode()
            if log_info_payment_mode:
                log_infos.append(log_info_payment_mode)
        if self.contact_payment_term:
            payment_term, log_info_payment_term = self._check_payment_term()
            if log_info_payment_term:
                log_infos.append(log_info_payment_term)
        if self.contact_account_fiscal_position:
            fiscal_position, log_info_position = self._check_fiscal_position()
            if log_info_position:
                log_infos.append(log_info_position)
        state = "error" if log_infos else "pass"
        action = "update" if state != "error" else "nothing"
        update_values.update(
            {
                "contact_id": contact and contact.id,
                "payment_mode_id": payment_mode and payment_mode.id,
                "payment_term_id": payment_term and payment_term.id,
                "account_fiscal_position_id": fiscal_position and fiscal_position.id,
                "log_info": "\n".join(log_infos),
                "state": state,
                "action": action,
            }
        )
        return update_values

    def _action_process(self):
        update_values = super()._action_process()
        if self.action != "nothing":
            self.contact_id.with_company(self.import_id.company_id).write(
                self._partner_values()
            )
            update_values.update(
                {
                    "state": "done",
                }
            )
        return update_values

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
        contacts = contact_obj.search(search_domain)
        if not contacts:
            contacts = False
            log_info = _("No contact found.")
        elif len(contacts) > 1:
            contacts = False
            log_info = _("More than one contact found.")
        return contacts and contacts[:1], log_info

    def _check_payment_mode(self):
        self.ensure_one()
        log_info = ""
        if self.payment_mode_id:
            return self.payment_mode_id, log_info
        payment_mode_obj = self.env["account.payment.mode"]
        search_domain = [
            ("name", "=", self.contact_payment_mode),
            ("company_id", "=", self.import_id.company_id.id),
        ]
        if self.import_id.import_type == "sale":
            search_domain = expression.AND(
                [[("payment_type", "=", "inbound")], search_domain]
            )
        elif self.import_id.import_type == "purchase":
            search_domain = expression.AND(
                [[("payment_type", "=", "outbound")], search_domain]
            )
        payment_modes = payment_mode_obj.search(search_domain)
        if not payment_modes:
            payment_modes = False
            log_info = _("No payment mode found.")
        elif len(payment_modes) > 1:
            payment_modes = False
            log_info = _("More than one payment modes found.")
        return payment_modes and payment_modes[:1], log_info

    def _check_payment_term(self):
        self.ensure_one()
        log_info = ""
        if self.payment_term_id:
            return self.payment_term_id, log_info
        payment_term_obj = self.env["account.payment.term"]
        search_domain = [
            ("name", "=", self.contact_payment_term),
            "|",
            ("company_id", "=", self.import_id.company_id.id),
            ("company_id", "=", False),
        ]
        payment_terms = payment_term_obj.search(search_domain)
        if not payment_terms:
            payment_terms = False
            log_info = _("No payment term found.")
        elif len(payment_terms) > 1:
            payment_terms = False
            log_info = _("More than one payment terms found.")
        return payment_terms and payment_terms[:1], log_info

    def _check_fiscal_position(self):
        self.ensure_one()
        log_info = ""
        if self.account_fiscal_position_id:
            return self.account_fiscal_position_id, log_info
        fiscal_position_obj = self.env["account.fiscal.position"]
        search_domain = [
            ("name", "=", self.contact_account_fiscal_position),
            ("company_id", "=", self.import_id.company_id.id),
        ]
        fiscal_positions = fiscal_position_obj.search(search_domain)
        if not fiscal_positions:
            fiscal_positions = False
            log_info = _("No fiscal position found.")
        elif len(fiscal_positions) > 1:
            fiscal_positions = False
            log_info = _("More than one fiscal position found.")
        return fiscal_positions and fiscal_positions[:1], log_info

    def _partner_values(self):
        self.ensure_one()
        import_type = self.import_id.import_type
        partner_values = {}
        if self.payment_mode_id:
            payment_type = self.payment_mode_id.payment_type
            if import_type != "purchase" and payment_type == "inbound":
                partner_values.update(
                    {
                        "customer_payment_mode_id": self.payment_mode_id.id,
                    }
                )
            if import_type != "sale" and payment_type == "outbound":
                partner_values.update(
                    {
                        "supplier_payment_mode_id": self.payment_mode_id.id,
                    }
                )
        if self.payment_term_id:
            if import_type != "purchase":
                partner_values.update(
                    {
                        "property_payment_term_id": self.payment_term_id.id,
                    }
                )
            if import_type != "sale":
                partner_values.update(
                    {
                        "property_supplier_payment_term_id": self.payment_term_id.id,
                    }
                )
        if self.account_fiscal_position_id:
            partner_values.update(
                {
                    "property_account_position_id": self.account_fiscal_position_id.id,
                }
            )
        return partner_values

    def action_open_form(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id(
            "contact_payment_mode_import_wizard.res_partner_payment_import_line_form_action"
        )
        action["res_id"] = self.id
        return action
