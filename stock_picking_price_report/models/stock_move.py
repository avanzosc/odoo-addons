# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    move_amount = fields.Float(
        string="Amount",
        compute="_compute_move_amount",
    )

    def _compute_move_amount(self):
        for move in self:
            amount = 0
            if move.sale_line_id:
                if move.quantity_done > 0:
                    amount = move.quantity_done * move.sale_line_id.price_unit
                else:
                    amount = move.product_uom_qty * move.sale_line_id.price_unit
            move.move_amount = amount
