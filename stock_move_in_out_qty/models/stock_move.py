# Copyright 2025 Aner Arregi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    in_qty = fields.Float(
        string="Incoming Qty", compute="_compute_in_out_qty", store=True
    )
    out_qty = fields.Float(
        string="Outgoing Qty", compute="_compute_in_out_qty", store=True
    )
    dif_qty = fields.Float(
        string="Difference", compute="_compute_in_out_qty", store=True
    )

    @api.depends("move_line_ids.in_qty", "move_line_ids.out_qty")
    def _compute_in_out_qty(self):
        for move in self:
            move.in_qty = sum(move.move_line_ids.mapped("in_qty"))
            move.out_qty = sum(move.move_line_ids.mapped("out_qty"))
            move.dif_qty = move.in_qty + move.out_qty
