# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.model
    def create(self, values):
        line = super(ProductProduct, self).create(values)
        if values.get("company_id", False):
            company = self.env["res.company"].browse(values.get("company_id"))
            line.company_ids = [(4, company.id)]
        return line

    def write(self, values):
        if values.get("company_id", False):
            values.update({
                "company_ids": [(4, values.get("company_id"))],
            })
        return super(ProductProduct, self).write(values)
