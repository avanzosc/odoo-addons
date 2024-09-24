# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class StockMove(models.Model):
    _inherit = "stock.move"

    def _prepare_move_line_vals(self, quantity=None, reserved_quant=None):
        self.ensure_one()
        vals = super()._prepare_move_line_vals(
            quantity=quantity, reserved_quant=reserved_quant
        )
        if "reserved_uom_qty" in vals and vals.get("reserved_uom_qty", 0):
            vals["qty_done"] = vals.get("reserved_uom_qty")
        return vals

    def _do_unreserve(self):
        result = super()._do_unreserve()
        lines = self.move_line_ids.filtered(
            lambda x: not x.reserved_uom_qty and x.qty_done
        )
        if lines:
            lines.write({"qty_done": 0})
        return result
