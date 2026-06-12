# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def button_force_done_detailed_operations(self):
        result = super().button_force_done_detailed_operations()
        for move in self.move_ids_without_package:
            if move.purchase_line_id and move.purchase_line_id.lot_id:
                for line in move.move_line_ids:
                    line.lot_id = move.purchase_line_id.lot_id.id
        return result
