# Copyright 2022 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.addons.base_import_wizard.models.base_import import convert2str
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval


class ResPartnerImport(models.Model):
    _name = "res.partner.import"
    _inherit = "base.import"
    _description = "Wizard to import contacts"

    import_line_ids = fields.One2many(
        comodel_name="res.partner.import.line",
    )
    partner_count = fields.Integer(
        string="# Contacts",
        compute="_compute_partner_count",
    )

    def _get_line_values(self, row_values=False):
        self.ensure_one()
        values = super()._get_line_values(row_values=row_values)
        if row_values:
            partner_name = row_values.get("Name", "")
            partner_ref = row_values.get("Ref", "")
            partner_vat = row_values.get("VAT", "")
            partner_street = row_values.get("Street", "")
            partner_zip = row_values.get("ZIP", "")
            partner_city = row_values.get("City", "")
            partner_state = row_values.get("State", "")
            partner_country = row_values.get("Country", "")
            partner_phone = row_values.get("Phone", ""),
            partner_mobile = row_values.get("Mobile", "")
            partner_email = row_values.get("Email", "")
            partner_website = row_values.get("Website", "")
            log_info = ""
            if not partner_name:
                return {}
            values.update(
                {
                    "partner_name": partner_name,
                    "partner_ref": convert2str(partner_ref),
                    "partner_vat": convert2str(partner_vat),
                    "partner_street": partner_street,
                    "partner_zip": convert2str(partner_zip),
                    "partner_city": partner_city.title(),
                    "partner_state": partner_state.title(),
                    "partner_country": partner_country.title(),
                    "partner_phone": convert2str(partner_phone),
                    "partner_mobile": convert2str(partner_mobile),
                    "partner_email": partner_email,
                    "partner_website": partner_website,
                    "log_info": log_info,
                }
            )
        return values

    def _compute_partner_count(self):
        for record in self:
            record.partner_count = len(record.mapped("import_line_ids.partner_id"))

    def button_open_partner(self):
        self.ensure_one()
        contacts = self.mapped("import_line_ids.partner_id")
        action = self.env.ref("contacts.action_contacts")
        action_dict = action.read()[0] if action else {}
        domain = expression.AND(
            [[("id", "in", contacts.ids)], safe_eval(action.domain or "[]")]
        )
        action_dict.update({"domain": domain})
        return action_dict


class ResPartnerImportLine(models.Model):
    _name = "res.partner.import.line"
    _inherit = "base.import.line"
    _description = "Wizard lines to import contacts"

    @api.model
    def _get_selection_partner_type(self):
        return self.env["res.partner"].fields_get(allfields=["type"])["type"][
            "selection"
        ]

    def default_partner_type(self):
        default_dict = self.env["res.partner"].default_get(["type"])
        return default_dict.get("type")

    import_id = fields.Many2one(
        comodel_name="res.partner.import",
    )
    action = fields.Selection(
        string="Action",
        selection=[
            ("create", "Create"),
            ("update", "Update"),
            ("nothing", "Nothing"),
        ],
        default="nothing",
        states={"done": [("readonly", True)]},
        copy=False,
        required=True,
    )
    partner_name = fields.Char(
        string="Name",
        states={"done": [("readonly", True)]},
        copy=False,
        required=True,
    )
    partner_comercial = fields.Char(
        string="Trade Name",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    partner_ref = fields.Char(
        string="Reference",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    partner_vat = fields.Char(
        string="Tax ID",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    partner_website = fields.Char(
        string="Website Link",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    partner_type = fields.Selection(
        selection="_get_selection_partner_type",
        string="Contact Type",
        default=default_partner_type,
        states={"done": [("readonly", True)]},
        copy=False,
        required=True,
    )
    partner_street = fields.Char(
        string="Street",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    partner_street2 = fields.Char(string="Street 2")
    partner_zip = fields.Char(
        string="Zip",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    partner_city = fields.Char(
        string="City Name",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    partner_state = fields.Char(
        string="State Name",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    partner_country = fields.Char(
        string="Country Name",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    partner_email = fields.Char(
        string="Email",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    partner_phone = fields.Char(
        string="Phone",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    partner_mobile = fields.Char(
        string="Mobile",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    partner_is_company = fields.Boolean(
        string="Is a Company",
        default=False,
        states={"done": [("readonly", True)]},
        copy=False,
    )
    partner_id = fields.Many2one(
        string="Contact",
        comodel_name="res.partner",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    partner_zip_id = fields.Many2one(
        comodel_name="res.city.zip",
        string="City Zip",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    partner_city_id = fields.Many2one(
        comodel_name="res.city",
        string="City",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    partner_state_id = fields.Many2one(
        comodel_name="res.country.state",
        string="State",
        domain="[('country_id', '=?', partner_country_id)]",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    partner_country_id = fields.Many2one(
        comodel_name="res.country",
        string="Country",
        states={"done": [("readonly", True)]},
        copy=False,
    )

    def action_validate(self):
        super().action_validate()
        line_values = []
        for line in self.filtered(lambda l: l.state != "done"):
            country = country_state = city = False
            contact, log_info = line._check_partner()
            if not log_info and line.partner_country:
                country, log_info = line._check_country()
            if not log_info and line.partner_state:
                country_state, log_info = line._check_state(country=country)
            if not log_info and line.partner_city:
                city, log_info = line._check_partner_city(
                    state=country_state, country=country
                )
            if city and not country_state:
                country_state = city.state_id
            if country_state and not country:
                country = country_state.country_id
            state = "error" if log_info else "pass"
            action = "nothing"
            if contact and state != "error":
                action = "update"
            elif state != "error":
                action = "create"
            update_values = {
                "partner_id": contact and contact.id,
                "partner_country_id": country and country.id,
                "partner_state_id": country_state and country_state.id,
                "partner_city_id": city and city.id,
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
            if line.action == "create":
                partner, log_info = line._create_partner()
            elif line.action == "update":
                partner, log_info = line._update_partner()
            else:
                continue
            state = "error" if log_info else "done"
            line_values.append(
                (
                    1,
                    line.id,
                    {
                        "partner_id": partner.id,
                        "log_info": log_info,
                        "state": state,
                    },
                )
            )
        return line_values

    def _check_partner(self):
        self.ensure_one()
        partner_obj = self.env["res.partner"]
        search_domain = [("name", "=", self.partner_name)]
        log_info = ""
        if self.partner_ref:
            search_domain = expression.OR(
                [[("ref", "=", self.partner_ref)], search_domain]
            )
        if self.partner_vat:
            search_domain = expression.OR(
                [[("vat", "=", self.partner_vat)], search_domain]
            )
        contacts = partner_obj.search(search_domain)
        if len(contacts) > 1:
            contacts = False
            log_info = _("Error: More than one contact already exist")
        return contacts and contacts[:1], log_info

    def _check_country(self):
        self.ensure_one()
        log_info = ""
        if self.partner_country_id:
            return self.partner_country_id, log_info
        country_obj = self.env["res.country"]
        search_domain = [("name", "=", self.partner_country)]
        countries = country_obj.search(search_domain)
        if len(countries) > 1:
            countries = False
            log_info = _("Error: More than one country already exist")
        return countries and countries[:1], log_info

    def _check_state(self, country=False):
        self.ensure_one()
        log_info = ""
        if self.partner_state_id:
            return self.partner_state_id, log_info
        state_obj = self.env["res.country.state"]
        search_domain = [("name", "=", self.partner_state)]
        if country:
            search_domain = expression.AND(
                [[("country_id", "=", country.id)], search_domain]
            )
        states = state_obj.search(search_domain)
        if len(states) > 1:
            states = False
            log_info = _(
                "Error: More than one state with name {} already exist"
            ).format(self.partner_state)
        return states and states[:1], log_info

    def _check_partner_city(self, state=False, country=False):
        self.ensure_one()
        log_info = ""
        if self.partner_city_id:
            return self.partner_city_id, log_info
        city_obj = self.env["res.city"]
        search_domain = [("name", "=", self.partner_city)]
        if state:
            search_domain = expression.AND(
                [[("state_id", "=", state.id)], search_domain]
            )
        if country:
            search_domain = expression.AND(
                [[("country_id", "=", country.id)], search_domain]
            )
        cities = city_obj.search(search_domain)
        if len(cities) > 1:
            cities = False
            log_info = _("Error: More than one city with name {} already exist").format(
                self.partner_city
            )
        return cities and cities[:1], log_info

    def _create_partner(self):
        self.ensure_one()
        contact, log_info = self._check_partner()
        if not contact and not log_info:
            contact_obj = self.env["res.partner"]
            values = self._partner_values()
            contact = contact_obj.with_context(no_vat_validation=True).create(values)
            log_info = ""
        return contact, log_info

    def _update_partner(self):
        self.ensure_one()
        values = self._partner_values()
        self.partner_id.with_context(no_vat_validation=True).write(values)
        log_info = ""
        return self.partner_id, log_info

    def _partner_values(self):
        return {
            "name": self.partner_name,
            "ref": self.partner_ref or self.partner_id.ref,
            "vat": self.partner_vat or self.partner_id.vat,
            "street": self.partner_street or self.partner_id.street,
            "zip": self.partner_zip or self.partner_id.zip,
            "city": self.partner_city or self.partner_id.city,
            "state_id": self.partner_state_id.id or self.partner_id.state_id.id,
            "country_id": self.partner_country_id.id or self.partner_id.country_id.id,
            "phone": self.partner_phone or self.partner_id.phone,
            "mobile": self.partner_mobile or self.partner_id.mobile,
            "email": self.partner_email or self.partner_id.email,
            "website": self.partner_website or self.partner_id.website,
        }

    @api.onchange("partner_city_id")
    def onchange_partner_city_id(self):
        for record in self:
            record.partner_state_id = record.partner_city_id.state_id

    @api.onchange("partner_state_id")
    def onchange_partner_state_id(self):
        for record in self:
            record.partner_country_id = record.partner_state_id.country_id

    # @api.onchange("partner_id")
    # def onchange_partner_id(self):
    #     for record in self:
