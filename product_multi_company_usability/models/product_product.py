# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.model
    def create(self, values):
        line = super().create(values)
        if "company_id" in values and values.get("company_id", False):
            company = self.env["res.company"].browse(values.get("company_id"))
            line.company_ids = [(4, company.id)]
        return line

    def write(self, values):
        result = super().write(values)
        if "company_id" in values and values.get("company_id", False):
            for line in self:
                if line.company_id:
                    line.company_ids = [(4, line.company_id.id)]
        return result
