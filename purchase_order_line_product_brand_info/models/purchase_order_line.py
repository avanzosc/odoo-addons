# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    product_brand_code = fields.Char()
    product_brand_id = fields.Many2one(comodel_name="product.brand")

    @api.onchange("seller_id")
    def onchange_seller_id(self):
        result = super().onchange_seller_id()
        if self.seller_id.brand_code:
            self.product_brand_code = self.seller_id.brand_code
        if self.seller_id.product_brand_id:
            self.product_brand_id = self.seller_id.product_brand_id.id
        return result
