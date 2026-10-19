# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.depends("product_id", "product_to_repair_id")
    def _compute_product_customer_code(self):
        result = super()._compute_product_customer_code()
        for line in self.filtered(lambda x: x.product_to_repair_id):
            supplierinfo = line.product_to_repair_id._select_customerinfo(
                partner=line.order_partner_id
            )
            line.product_customer_code = supplierinfo.product_code
        return result
