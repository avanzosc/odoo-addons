# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.addons.base_import_wizard.models.base_import import convert2str
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval


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
        required=True)

    def _get_line_values(self, row_values=False):
        self.ensure_one()
        values = super()._get_line_values(row_values=row_values)
        if row_values:
            contact_name = row_values.get("Name", "")
            contact_code = row_values.get("Code", "")
            contact_description = row_values.get("Description", "")
            contact_phone = row_values.get("Phone", "")
            contact_email = row_values.get("Email", "")
            log_info = ""
            if not contact_name and not contact_code:
                return {}
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
            record.res_partner_count = len(
                record.mapped("import_line_ids.contact_id"))

    def button_open_res_partner(self):
        self.ensure_one()
        contacts = self.mapped("import_line_ids.contact_id")
        action = self.env.ref("contacts.action_contacts")
        action_dict = action.read()[0] if action else {}
        domain = expression.AND(
            [[("id", "in", contacts.ids)], safe_eval(action.domain or "[]")])
        action_dict.update({"domain": domain})
        return action_dict


class ResPartnerPhoneImportLine(models.Model):
    _name = "res.partner.phone.import.line"
    _inherit = "base.import.line"
    _description = "Lines to import contacts extra phone"

    @api.model
    def _get_selection_contact_type(self):
        return self.env["res.partner"].fields_get(
            allfields=["type"])["type"]["selection"]

    def default_contact_type(self):
        default_dict = self.env["res.partner"].default_get(["type"])
        return default_dict.get("type")

    import_id = fields.Many2one(
        comodel_name="res.partner.phone.import",
    )
    action = fields.Selection(
        string="Action",
        selection=[
            ("update", "Update"),
            ("nothing", "Nothing"),
        ],
        default="nothing",
        states={"done": [("readonly", True)]},
        copy=False,
        required=True,
    )
    contact_id = fields.Many2one(
        string="Contact",
        comodel_name="res.partner")
    contact_name = fields.Char(
        string="Contact Name",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    contact_code = fields.Char(
        string="Contact Code",
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

    def action_validate(self):
        super().action_validate()
        line_values = []
        for line in self.filtered(lambda l: l.state != "done"):
            log_info = ""
            contact = False
            if line.contact_name or line.contact_code:
                contact, log_info_contact = line._check_contact()
                if log_info_contact:
                    log_info += log_info_contact
            state = "error" if log_info else "pass"
            action = "nothing"
            if state != "error":
                action = "update"
            update_values = {
                "contact_id": contact and contact.id,
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
        for line in self.filtered(lambda l: l.state not in ("error", "done")):
            if line.action == "update":
                contact, log_info = line._check_contact()
                if contact:
                    contact.extra_phone_ids = [(0, 0, {
                        "description": line.contact_description,
                        "phone": line.contact_phone,
                        "email": line.contact_email})]
            else:
                continue
            state = "error" if log_info else "done"
            line.write({
                "contact_id": contact.id,
                "log_info": log_info,
                "state": state})
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
        search_domain = [("company_id", "=", self.import_id.company_id.id)]
        if self.contact_code:
            search_domain = [
                ("ref", "like", self.contact_code)]
        else:
            search_domain = [
                ("company_id", "=", self.import_id.company_id.id),
                ("name", "=", self.contact_name)]
        contacts = contact_obj.search(search_domain)
        if not contacts:
            contacts = False
            log_info = _("Error: No contact found.")
        elif len(contacts) > 1:
            contacts = False
            log_info = _("Error: More than one contact found.")
        return contacts and contacts[:1], log_info
