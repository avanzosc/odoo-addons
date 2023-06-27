# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, fields, models
from odoo.addons.base_import_wizard.models.base_import import convert2str


class ProductImport(models.Model):
    _inherit = "product.import"

    def _get_line_values(self, row_values={}):
        self.ensure_one()
        values = super()._get_line_values(row_values=row_values)
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

    hs_code = fields.Char(
        string="HS Code Name")
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

    def action_validate(self):
        result = super(ProductImportLine, self).action_validate()
        for line in self.filtered(lambda l: l.state != "done"):
            log_info = ""
            hs_code = country = False
            if line.hs_code:
                hs_code, log_info_hs_code = line._check_hs_code()
                if log_info_hs_code:
                    log_info += log_info_hs_code
            if line.origin_country:
                country, log_info_country = line._check_country()
                if log_info_country:
                    log_info += log_info_country
            if log_info:
                line.log_info += log_info
            result.append(
                (
                    1,
                    line.id,
                    {
                        "hs_code_id": hs_code and hs_code.id,
                        "origin_country_id": country and country.id,
                    },
                )
            )
        return result

    def _check_hs_code(self):
        self.ensure_one()
        log_info = ""
        if self.hs_code_id:
            return self.hs_code_id, log_info
        hs_code_obj = self.env["hs.code"]
        search_domain = [("local_code", "ilike", self.hs_code)]
        hs_codes = hs_code_obj.search(search_domain)
        if not hs_codes:
            hs_codes = hs_code_obj.create({
                "local_code": self.hs_code,
                "company_id": self.import_id.company_id.id})
        elif len(hs_codes) > 1:
            hs_codes = False
            log_info = _("Error: More than one HS code found.")
        return hs_codes, log_info

    def _check_country(self):
        self.ensure_one()
        log_info = ""
        if self.origin_country_id:
            return self.origin_country_id, log_info
        country_obj = self.env["res.country"]
        search_domain = [("name", "ilike", self.origin_country)]
        countries = country_obj.search(search_domain)
        if not countries:
            log_info = _("Error: No country found.")
        elif len(countries) > 1:
            countries = False
            log_info = _("Error: More than one country found.")
        return countries[:1], log_info

    def _product_values(self):
        self.ensure_one()
        result = super(ProductImportLine, self)._product_values()
        result.update({
            "hs_code_id": self.hs_code_id.id,
            "origin_country_id": self.origin_country_id.id
            })
        return result
