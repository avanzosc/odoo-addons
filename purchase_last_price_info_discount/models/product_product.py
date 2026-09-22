# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    last_purchase_discount = fields.Float(
        string="Last Purchase Discount (%)",
        digits="Discount",
        compute="_compute_last_purchase_line_id_info",
    )
    last_purchase_net_unit_price = fields.Float(
        compute="_compute_last_purchase_line_id_info",
    )

    @api.depends("last_purchase_line_id")
    def _compute_last_purchase_line_id_info(self):
        result = super()._compute_last_purchase_line_id_info()
        for item in self:
            item.last_purchase_discount = item.last_purchase_line_id.discount
            if item.last_purchase_line_id.discount:
                item.last_purchase_net_unit_price = (
                    item.last_purchase_line_id.price_unit
                    - (
                        item.last_purchase_line_id.price_unit
                        * (item.last_purchase_line_id.discount / 100)
                    )
                )
            else:
                item.last_purchase_net_unit_price = item.last_purchase_price
        return result
