# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, fields, models
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval

from odoo.addons.base_import_wizard.models.base_import import convert2str


class ResPartnerPhoneImport(models.Model):
    _name = "res.partner.phone.import"
    _inherit = "base.import"
    _description = "Wizard to import contact extra phone"

    import_line_ids = fields.One2many(
        comodel_name="res.partner.phone.import.line",
    )
    res_partner_count = fields.Integer(
        string="# Contacts",
        compute="_compute_res_partner_count",
    )
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
    )

    def _get_line_values(self, row_values, datemode=False):
        self.ensure_one()
        values = super()._get_line_values(row_values, datemode=datemode)
        if row_values:
            contact_name = row_values.get("Name", "")
            contact_code = row_values.get("Code", "")
            contact_description = row_values.get("Description", "")
            contact_phone = row_values.get("Phone", "")
            contact_email = row_values.get("Email", "")
            log_info = ""
            if contact_name or contact_code:
                values.update(
                    {
                        "contact_name": contact_name.title(),
                        "contact_code": convert2str(contact_code),
                        "contact_description": convert2str(contact_description),
                        "contact_phone": convert2str(contact_phone),
                        "contact_email": convert2str(contact_email),
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


class ResPartnerPhoneImportLine(models.Model):
    _name = "res.partner.phone.import.line"
    _inherit = "base.import.line"
    _description = "Lines to import contacts extra phone"

    import_id = fields.Many2one(
        comodel_name="res.partner.phone.import",
    )
    action = fields.Selection(
        selection_add=[
            ("create", "Create"),
        ],
        ondelete={"create": "set default"},
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
    contact_description = fields.Char(
        string="Description",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    contact_phone = fields.Char(
        string="Phone",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    contact_email = fields.Char(
        string="Email",
        states={"done": [("readonly", True)]},
        copy=False,
    )

    def _action_validate(self):
        update_values = super()._action_validate()
        if self.contact_name or self.contact_code:
            contact, log_info = self._check_contact()
        state = "error" if log_info else "pass"
        action = "create" if state != "error" else "nothing"
        update_values.update(
            {
                "contact_id": contact and contact.id,
                "log_info": log_info,
                "state": state,
                "action": action,
            }
        )
        return update_values

    def _action_process(self):
        update_values = super()._action_process()
        if self.action != "nothing":
            self._create_extra_phone()
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
        search_domain = [
            "|",
            ("company_id", "=", self.import_id.company_id.id),
            ("company_id", "=", False),
        ]
        if self.contact_code:
            search_domain = expression.AND(
                [
                    [
                        ("ref", "like", self.contact_code),
                    ],
                    search_domain,
                ]
            )
        else:
            search_domain = expression.AND(
                [
                    [
                        ("name", "=", self.contact_name),
                    ],
                    search_domain,
                ]
            )
        contacts = contact_obj.search(search_domain)
        if not contacts:
            log_info = _("No contact found.")
        elif len(contacts) > 1:
            contacts = False
            log_info = _("More than one contact found.")
        return contacts and contacts[:1], log_info

    def _create_extra_phone(self):
        self.ensure_one()
        self.sudo().env["extra.phone"].create(self._extra_phone_values())
        return True

    def _extra_phone_values(self):
        self.ensure_one()
        return {
            "partner_id": self.contact_id.id,
            "description": self.contact_description,
            "phone": self.contact_phone,
            "email": self.contact_email,
        }
