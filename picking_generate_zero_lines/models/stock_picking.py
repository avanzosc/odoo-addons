# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def button_validate(self):
        zero_moves = self.move_ids_without_package.filtered(
            lambda c: c.quantity_done == 0
        )
        for move in zero_moves:
            move.write(
                {
                    "state": "done",
                    "product_uom_qty": move.quantity_done,
                }
            )
            if not move.move_line_ids:
                self.env["stock.move.line"].create(move._prepare_move_line_vals())
        result = super(StockPicking, self).button_validate()
        return result
