# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    def write(self, values):
        result = super().write(values)
        if "price_unit" in values and values.get("price_unit", False):
            for line in self:
                product = line.mapped("product_id")
                if line.state in ("draft", "cancel"):
                    product.set_product_last_purchase()
                else:
                    product.set_product_last_purchase(line.order_id.id)
        return result
