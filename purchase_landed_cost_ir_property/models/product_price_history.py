# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, models


class ProductPriceHistory(models.Model):
    _inherit = "product.price.history"

    @api.model
    def create(self, values):
        if "product_id" in values:
            product = self.env["product.product"].browse(values.get("product_id"))
            if product.company_id:
                values["company_id"] = product.company_id.id
        return super(ProductPriceHistory, self).create(values)
