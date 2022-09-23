# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    last_purchase_discount = fields.Float(
        string="Last Purchase Discount (%)", digits="Discount",
        compute="_compute_last_purchase_line_id_info")
    last_purchase_net_unit_price = fields.Float(
        string="Last Purchase Net Unit Price",
        compute="_compute_last_purchase_line_id_info",)

    @api.depends("last_purchase_line_id")
    def _compute_last_purchase_line_id_info(self):
        result = super(
            ProductTemplate, self)._compute_last_purchase_line_id_info()
        for item in self:
            item.last_purchase_discount = item.last_purchase_line_id.discount
            if item.last_purchase_line_id.product_qty:
                item.last_purchase_net_unit_price = (
                    item.last_purchase_line_id.price_subtotal /
                    item.last_purchase_line_id.product_qty)
            else:
                item.last_purchase_net_unit_price = item.last_purchase_price
        return result
