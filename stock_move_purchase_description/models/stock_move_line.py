# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    def _get_aggregated_properties(self, move_line=False, move=False):
        aggregated_properties = super()._get_aggregated_properties(
            move_line=move_line, move=move
        )
        move = move or (move_line.move_id if move_line else self.env["stock.move"])
        if move and move.picking_code == "incoming":
            aggregated_properties["name"] = move.name
        return aggregated_properties
