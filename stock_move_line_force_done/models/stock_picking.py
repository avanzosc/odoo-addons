# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def button_force_done_detailed_operations(self):
        move_line_obj = self.env["stock.move.line"]
        for picking in self:
            pending_move_lines = picking.move_line_ids.filtered(
                lambda l: not l.move_id)
            pending_move_lines.unlink()
            for move in picking.move_lines:
                if not move.move_line_ids:
                    move_line_obj.create(move._prepare_move_line_vals())
                line = move.move_line_ids[:1]
                if line and line.qty_done != move.product_uom_qty:
                    line.qty_done = move.product_uom_qty
