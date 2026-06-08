# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, fields, models

from odoo.addons.base_import_wizard.models.base_import import convert2str


class ProductImport(models.Model):
    _inherit = "product.import"

    def _get_line_values(self, row_values, datemode=False):
        self.ensure_one()
        values = super()._get_line_values(row_values, datemode=datemode)
        if values and row_values:
            hs_code = row_values.get("HS Code", "")
            origin_country = row_values.get("Origin Country", "")
            values.update(
                {
                    "hs_code": convert2str(hs_code),
                    "origin_country": origin_country,
                }
            )
        return values


class ProductImportLine(models.Model):
    _inherit = "product.import.line"

    hs_code = fields.Char(string="HS Code Name")
    hs_code_id = fields.Many2one(
        string="HS Code",
        comodel_name="hs.code",
        domain="[('local_code', 'ilike', hs_code)]",
    )
    origin_country = fields.Char(
        string="Origin Country Name",
    )
    origin_country_id = fields.Many2one(
        string="Origin Country",
        comodel_name="res.country",
        domain="[('name', 'ilike', origin_country)]",
    )

    def _action_validate(self):
        update_values = super()._action_validate()
        log_infos = (
            [update_values.get("log_info")]
            if update_values.get("log_info", False)
            else []
        )
        hs_code = country = False
        if self.hs_code:
            hs_code, log_info_code = self._check_hs_code()
            if log_info_code:
                log_infos.append(log_info_code)
        if self.origin_country:
            country, log_info_country = self._check_country()
            if log_info_country:
                log_infos.append(log_info_country)
        state = "error" if log_infos else "pass"
        action = "nothing"
        if update_values.get("product_id", False) and state != "error":
            action = "update"
        elif state != "error":
            action = "create"
        update_values.update(
            {
                "hs_code_id": hs_code and hs_code.id,
                "origin_country_id": country and country.id,
                "log_info": "\n".join(log_infos),
                "state": state,
                "action": action,
            }
        )
        return update_values

    def _check_hs_code(self):
        self.ensure_one()
        log_info = ""
        if self.hs_code_id:
            return self.hs_code_id, log_info
        hs_code_obj = self.env["hs.code"]
        search_domain = [("local_code", "ilike", self.hs_code)]
        hs_codes = hs_code_obj.search(search_domain)
        if not hs_codes:
            hs_codes = hs_code_obj.create(
                {
                    "local_code": self.hs_code,
                    "company_id": self.import_id.company_id.id,
                }
            )
        elif len(hs_codes) > 1:
            hs_codes = False
            log_info = _("More than one HS code found.")
        return hs_codes and hs_codes[:1], log_info

    def _check_country(self):
        self.ensure_one()
        log_info = ""
        if self.origin_country_id:
            return self.origin_country_id, log_info
        country_obj = self.env["res.country"]
        search_domain = [("name", "ilike", self.origin_country)]
        countries = country_obj.search(search_domain)
        if not countries:
            log_info = _("No country found.")
        elif len(countries) > 1:
            countries = False
            log_info = _("More than one country found.")
        return countries and countries[:1], log_info

    def _product_values(self):
        self.ensure_one()
        values = super()._product_values()
        values.update(
            {
                "hs_code_id": self.hs_code_id.id,
                "origin_country_id": self.origin_country_id.id,
            }
        )
        return values
