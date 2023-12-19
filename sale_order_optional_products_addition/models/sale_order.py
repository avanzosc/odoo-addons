# Copyright 2020 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _delete_optional_lines(self):
        lines_dict = []
        for optional_line in self.sale_order_option_ids:
            lines_dict.append((2, optional_line.id))
        return lines_dict

    @api.onchange('order_line')
    def onchange_order_line(self):
        self.sale_order_option_ids = self._delete_optional_lines()
        optional_products = []
        for line in self.order_line:
            product = line.product_id
            if line.product_id:
                for optional in product.optional_product_product_ids:
                    optional_products.append((0, 0, {
                        'product_id': optional.id,
                        'name': optional.description_sale or optional.name,
                        'quantity': "1",
                        'uom_id': optional.uom_id,
                        'price_unit': optional.list_price,
                    }))
        self.sale_order_option_ids = optional_products
