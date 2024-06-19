# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.model
    def create(self, values):
        if values.get("company_id", False):
            values.update({
                "company_ids": [(4, values.get("company_id"))],
            })
        return super(ProductProduct, self).create(values)

    def write(self, values):
        if values.get("company_id", False):
            values.update({
                "company_ids": [(4, values.get("company_id"))],
            })
        return super(ProductProduct, self).write(values)
