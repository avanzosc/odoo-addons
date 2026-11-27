# Copyright 2026 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    def _prepare_new_lot_vals(self):
        """Copy the dimensional information of the purchase order line to the
        lot created on reception."""
        vals = super()._prepare_new_lot_vals()
        line = self.move_id.purchase_line_id
        if line:
            vals.update(
                {
                    "purchase_pricing_method": line.pricing_method,
                    "theoretical_length": line.purchase_length,
                    "theoretical_weight": line.purchase_weight,
                    "purchase_length": line.product_length,
                    "purchase_length_uom_id": line.purchase_length_uom_id.id,
                    "purchase_weight": line.product_weight,
                    "purchase_weight_uom_id": line.purchase_weight_uom_id.id,
                }
            )
        return vals
