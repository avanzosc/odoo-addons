# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _prepare_invoice_line(self, **optional_values):
        result = super()._prepare_invoice_line(**optional_values)
        product_packaging_qty = 0
        if self.product_packaging_qty and self.product_uom_qty and self.qty_to_invoice:
            product_packaging_qty = (
                self.qty_to_invoice * self.product_packaging_qty
            ) / self.product_uom_qty
        result["product_packaging_qty"] = product_packaging_qty
        return result
