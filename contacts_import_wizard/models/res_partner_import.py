# Copyright 2022 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval

from odoo.addons.base_import_wizard.models.base_import import convert2str


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
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        index=True,
    )

    def _get_line_values(self, row_values, datemode=False):
        self.ensure_one()
        values = super()._get_line_values(row_values, datemode=datemode)
        if row_values:
            partner_name = row_values.get("Name", "")
            partner_comercial = row_values.get("Trade Name", "")
            partner_parent = row_values.get("Parent", "")
            partner_type = row_values.get("Type", "")
            if not partner_type:
                partner_type = "other"
            partner_ref = row_values.get("Code", "")
            partner_vat = row_values.get("VAT", "")
            partner_street = row_values.get("Street", "")
            partner_street2 = row_values.get("Street2", "")
            partner_zip = row_values.get("ZIP", "")
            partner_city = row_values.get("City", "")
            partner_state = row_values.get("State", "")
            partner_country = row_values.get("Country", "")
            partner_phone = row_values.get("Phone", "")
            partner_mobile = row_values.get("Mobile", "")
            partner_email = row_values.get("Email", "")
            partner_website = row_values.get("Website", "")
            partner_comment = row_values.get("Comment", "")
            partner_function = row_values.get("Function", "")
            partner_company_type = row_values.get("Company Type", "")
            if partner_parent and not partner_company_type:
                partner_company_type = "person"
            elif not partner_parent and not partner_company_type:
                partner_company_type = "company"
            log_info = ""
            if not partner_name:
                return {}
            values.update(
                {
                    "partner_name": partner_name,
                    "partner_comercial": partner_comercial,
                    "partner_parent_name": partner_parent,
                    "partner_type": partner_type,
                    "partner_ref": convert2str(partner_ref),
                    "partner_vat": convert2str(partner_vat),
                    "partner_street": partner_street,
                    "partner_street2": partner_street2,
                    "partner_zip": convert2str(partner_zip),
                    "partner_city": partner_city.title(),
                    "partner_state": partner_state.title(),
                    "partner_country": partner_country.title(),
                    "partner_phone": convert2str(partner_phone),
                    "partner_mobile": convert2str(partner_mobile),
                    "partner_email": partner_email,
                    "partner_website": partner_website,
                    "partner_comment": partner_comment,
                    "partner_function": partner_function,
                    "partner_company_type": partner_company_type,
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
        action = self.env["ir.actions.actions"]._for_xml_id("contacts.action_contacts")
        action["domain"] = expression.AND(
            [[("id", "in", contacts.ids)], safe_eval(action.get("domain") or "[]")]
        )
        action["context"] = dict(self._context, create=False)
        return action


class ResPartnerImportLine(models.Model):
    _name = "res.partner.import.line"
    _inherit = "base.import.line"
    _description = "Wizard lines to import contacts"

    @api.model
    def _get_selection_partner_type(self):
        return self.env["res.partner"].fields_get(allfields=["type"])["type"][
            "selection"
        ]

    @api.model
    def _get_selection_partner_company_type(self):
        return self.env["res.partner"].fields_get(allfields=["company_type"])[
            "company_type"
        ]["selection"]

    def default_partner_type(self):
        default_dict = self.env["res.partner"].default_get(["type"])
        return default_dict.get("type")

    def default_partner_company_type(self):
        default_dict = self.env["res.partner"].default_get(["company_type"])
        return default_dict.get("company_type")

    import_id = fields.Many2one(
        comodel_name="res.partner.import",
    )
    action = fields.Selection(
        selection_add=[
            ("update", "Update"),
            ("create", "Create"),
        ],
        ondelete={"update": "set default", "create": "set default"},
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
    partner_parent_name = fields.Char(
        string="Parent Name",
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
    partner_street2 = fields.Char(
        string="Street 2",
        states={"done": [("readonly", True)]},
        copy=False,
    )
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
    partner_comment = fields.Text(
        string="Notes",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    partner_id = fields.Many2one(
        string="Contact",
        comodel_name="res.partner",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    partner_parent_id = fields.Many2one(
        string="Related Company",
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
    partner_function = fields.Char(
        string="Function",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    partner_company_type = fields.Selection(
        selection="_get_selection_partner_company_type",
        string="Company Type",
        default=default_partner_company_type,
        states={"done": [("readonly", True)]},
        copy=False,
    )

    def _action_validate(self):
        update_values = super()._action_validate()
        log_infos = []
        if self.import_id.company_id:
            self = self.with_company(self.import_id.company_id)
        parent = country = country_state = city = zip_info = False
        log_info_city = log_info_zip = log_info_state = log_info_country = ""
        contact, log_info_contact = self._check_partner()
        if log_info_contact:
            log_infos.append(log_info_contact)
        if self.partner_parent_name:
            parent, log_info_parent = self._check_partner_parent()
            if log_info_parent:
                log_infos.append(log_info_parent)
        if self.partner_country:
            country, log_info_country = self._check_country()
        if self.partner_state:
            country_state, log_info_state = self._check_state(country=country)
        if self.partner_zip:
            zip_info, log_info_zip = self._check_zip(
                state=country_state, country=country
            )
        if zip_info and not city:
            city = zip_info.city_id
        if not city and self.partner_city:
            city, log_info_city = self._check_partner_city(
                state=country_state, country=country
            )
        if city and not country_state:
            country_state = city.state_id
        if country_state and not country:
            country = country_state.country_id
        if not city:
            if log_info_city:
                log_infos.append(log_info_city)
            if log_info_zip:
                log_infos.append(log_info_zip)
        if not country_state and log_info_state:
            log_infos.append(log_info_state)
        if not country and log_info_country:
            log_infos.append(log_info_country)
        state = "error" if log_infos else "pass"
        action = "nothing"
        if contact and state != "error":
            action = "update"
        elif state != "error":
            action = "create"
        update_values.update(
            {
                "partner_id": contact and contact.id,
                "partner_parent_id": parent and parent.id,
                "partner_country_id": country and country.id,
                "partner_state_id": country_state and country_state.id,
                "partner_city_id": city and city.id,
                "partner_zip_id": zip_info and zip_info.id,
                "log_info": "\n".join(log_infos),
                "state": state,
                "action": action,
            }
        )
        return update_values

    def _action_process(self):
        update_values = super()._action_process()
        if self.action != "nothing":
            if self.import_id.company_id:
                self = self.with_company(self.import_id.company_id)
            if self.action == "create":
                partner, log_info = self._create_partner()
            elif self.action == "update":
                partner, log_info = self._update_partner()
            state = "error" if log_info else "done"
            update_values.update(
                {
                    "partner_id": partner and partner.id,
                    "log_info": log_info,
                    "state": state,
                }
            )
        return update_values

    def _check_partner(self):
        self.ensure_one()
        log_info = ""
        partner_obj = self.env["res.partner"]
        if self.import_id.company_id:
            partner_obj = partner_obj.with_company(self.import_id.company_id)
        if self.partner_id:
            return self.partner_id, log_info
        search_domain = [("name", "=", self.partner_name)]
        if self.partner_ref and not self.partner_parent_name:
            search_domain = expression.OR(
                [[("ref", "=", self.partner_ref)], search_domain]
            )
        if self.partner_vat and not self.partner_parent_name:
            search_domain = expression.OR(
                [[("vat", "=", self.partner_vat)], search_domain]
            )
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
        contacts = partner_obj.search(search_domain)
        if len(contacts) > 1:
            contacts = False
            log_info = _("More than one contact already exist")
        return contacts and contacts[:1], log_info

    def _check_partner_parent(self):
        self.ensure_one()
        log_info = ""
        partner_obj = self.env["res.partner"]
        if self.import_id.company_id:
            partner_obj = partner_obj.with_company(self.import_id.company_id)
        search_domain = [("name", "=", self.partner_parent_name)]
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
        contacts = partner_obj.search(search_domain)
        if len(contacts) > 1:
            contacts = False
            log_info = _(
                "More than one contact already exist, unable to select one parent"
            )
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
            log_info = _("More than one country already exist")
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
            log_info = _("More than one state with name {} already exist").format(
                self.partner_state
            )
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
            log_info = _("More than one city with name {} already exist").format(
                self.partner_city
            )
        return cities and cities[:1], log_info

    def _check_zip(self, state=False, country=False):
        self.ensure_one()
        log_info = ""
        if self.partner_zip_id:
            return self.partner_zip_id, log_info
        zip_obj = self.env["res.city.zip"]
        search_domain = [("name", "=", self.partner_zip)]
        if state:
            search_domain = expression.AND(
                [[("city_id.state_id", "=", state.id)], search_domain]
            )
        if country:
            search_domain = expression.AND(
                [[("city_id.country_id", "=", country.id)], search_domain]
            )
        zips = zip_obj.search(search_domain)
        if len(zips) > 1:
            zips = zips.filtered(lambda z: z.city_id.name == self.partner_city)
        if len(zips) > 1:
            zips = False
            log_info = _("More than one city with zip {} already exist").format(
                self.partner_zip
            )
        return zips and zips[:1], log_info

    def _create_partner(self):
        self.ensure_one()
        contact, log_info = self._check_partner()
        if not contact and not log_info:
            contact = (
                self.env["res.partner"]
                .with_context(
                    no_vat_validation=True,
                    default_company_id=self.import_id.company_id.id,
                )
                .create(self._partner_values())
            )
            log_info = ""
        return contact, log_info

    def _update_partner(self):
        self.ensure_one()
        values = self._partner_values()
        self.partner_id.with_company(self.import_id.company_id).with_context(
            no_vat_validation=True
        ).write(values)
        return self.partner_id, ""

    def _partner_values(self):
        return {
            "name": self.partner_name,
            "comercial": self.partner_comercial or self.partner_id.comercial,
            "parent_id": self.partner_parent_id.id or self.partner_id.parent_id.id,
            "company_type": self.partner_company_type or self.partner_id.company_type,
            "type": self.partner_type or self.partner_id.type,
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
            "comment": self.partner_comment or self.partner_id.comment,
        }

    @api.onchange("partner_city_id")
    def onchange_partner_city_id(self):
        for record in self:
            record.partner_state_id = record.partner_city_id.state_id

    @api.onchange("partner_state_id")
    def onchange_partner_state_id(self):
        for record in self:
            record.partner_country_id = record.partner_state_id.country_id

    def action_open_form(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id(
            "contacts_import_wizard.res_partner_import_line_form_action"
        )
        action["res_id"] = self.id
        return action
