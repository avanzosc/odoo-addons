# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models
from odoo.tools.float_utils import float_compare


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def button_force_done_detailed_operations(self):
        move_line_obj = self.env["stock.move.line"]
        for picking in self:
            pending_move_lines = picking.move_line_ids.filtered(
                lambda move_line: not move_line.move_id
            )
            pending_move_lines.unlink()
            for move in picking.move_ids:
                if not move.move_line_ids:
                    move_line_obj.create(move._prepare_move_line_vals())
                line = move.move_line_ids[:1]
                if line:
                    demanded_qty = move.product_uom._compute_quantity(
                        move.product_uom_qty, line.product_uom_id, round=False
                    )
                    if (
                        float_compare(
                            line.quantity,
                            demanded_qty,
                            precision_rounding=line.product_uom_id.rounding,
                        )
                        != 0
                    ):
                        line.quantity = demanded_qty
