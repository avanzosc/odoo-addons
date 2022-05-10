# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_force_done_detailed_operations(self):
        for picking in self:
            for move in picking.move_ids_without_package:
                lines = picking.move_line_ids_without_package.filtered(
                    lambda x: not x.move_id)
                if lines:
                    lines.unlink()
                line = picking.move_line_ids_without_package.filtered(
                    lambda x: x.move_id == move)
                if not line:
                    line = self.env['stock.move.line'].create(
                        move._prepare_move_line_vals())
                if line and line.qty_done != move.product_uom_qty:
                    line.qty_done = move.product_uom_qty
