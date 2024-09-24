# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    def write(self, vals):
        if (
            "bypass_reservation_update" in self.env.context
            and "reserved_uom_qty" in vals
            and vals.get("reserved_uom_qty", False)
        ):
            vals["qty_done"] = vals.get("reserved_uom_qty")
        return super().write(vals)
