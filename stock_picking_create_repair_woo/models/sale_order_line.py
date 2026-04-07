# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            product_id = vals.get("product_id", False)
            if not product_id:
                continue
            product = self.env["product.product"].browse(product_id)
            if product.is_repair and not vals.get("product_to_repair_id", False):
                if vals.get("order_id", False):
                    self._put_sale_order_type_in_sale_order(vals.get("order_id"))
                vals = self._catch_generic_repair_product(vals)
        return super().create(vals_list)

    def _put_sale_order_type_in_sale_order(self, order_id):
        sale_order = self.env["sale.order"].browse(order_id)
        if sale_order:
            cond = [("is_repair", "=", True)]
            sale_order_type = self.env["sale.order.type"].search(cond, limit=1)
            if sale_order_type and (
                not sale_order.type_id or not sale_order.type_id.is_repair
            ):
                sale_order.type_id = sale_order_type.id
                if sale_order_type.sequence_id:
                    sale_order.name = sale_order_type.sequence_id.next_by_id(
                        sequence_date=sale_order.date_order
                    )

    def _catch_generic_repair_product(self, vals):
        cond = [("generic_repair_product", "=", True)]
        generic_prepair_product = self.env["product.product"].search(cond, limit=1)
        if generic_prepair_product:
            vals["product_to_repair_id"] = generic_prepair_product.id
        return vals
