# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models


class StockMove(models.Model):
    _inherit = "stock.move"

    def write(self, vals):
        result = super().write(vals)
        if "state" in vals and vals.get("state", False) == "done":
            for move in self.filtered(
                lambda x: x.product_id.machine_ok
                and x.picking_type_id.code == "incoming"
            ):
                if move.move_line_ids:
                    move.move_line_ids.create_machine()
        return result
