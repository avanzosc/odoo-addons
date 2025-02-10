# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    def _compute_bosex_sacs(self):
        for move in self:
            boxes_sacks = 0
            if move.sale_line_id and move.sale_line_id.product_packaging_qty:
                packaging_qty = move.sale_line_id.product_packaging_qty
                product_uom_qty = move.sale_line_id.product_uom_qty
                boxes_sacks = (move.quantity_done * packaging_qty) / product_uom_qty
            move.boxes_sacks = boxes_sacks

    boxes_sacks = fields.Integer(string="Boxes/Sacks", compute="_compute_bosex_sacs")
    palet_qty = fields.Float(
        string="Contained Palet Quantity",
        digits="Product Unit of Measure",
        compute="_compute_palet_qty",
        store=True,
    )

    @api.depends("move_line_ids", "move_line_ids.palet_qty")
    def _compute_palet_qty(self):
        for move in self:
            if move.move_line_ids:
                move.palet_qty = sum(move.move_line_ids.mapped("palet_qty"))
            elif move.sale_line_id:
                move.palet_qty = move.sale_line_id.palet_qty
