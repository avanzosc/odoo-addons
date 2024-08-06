# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    def _compute_product_packaging_qty(self):
        for move in self:
            demand_product_packaging_qty = 0
            done_product_packaging_qty = 0
            if (
                move.sale_line_id
                and move.product_uom_qty
                and move.sale_line_id.product_packaging_qty
                and move.sale_line_id.product_uom_qty
            ):
                demand_product_packaging_qty = (
                    move.product_uom_qty * move.sale_line_id.product_packaging_qty
                ) / move.sale_line_id.product_uom_qty
            if (
                move.sale_line_id
                and move.quantity_done
                and move.sale_line_id.product_packaging_qty
                and move.sale_line_id.product_uom_qty
            ):
                done_product_packaging_qty = (
                    move.quantity_done * move.sale_line_id.product_packaging_qty
                ) / move.sale_line_id.product_uom_qty
            move.demand_product_packaging_qty = demand_product_packaging_qty
            move.done_product_packaging_qty = done_product_packaging_qty

    def _compute_bosex_sacs(self):
        for move in self:
            boxes_sacks = 0
            if move.sale_line_id and move.sale_line_id.product_packaging_qty:
                packaging_qty = move.sale_line_id.product_packaging_qty
                product_uom_qty = move.sale_line_id.product_uom_qty
                boxes_sacks = (move.quantity_done * packaging_qty) / product_uom_qty
            move.boxes_sacks = boxes_sacks

    demand_product_packaging_qty = fields.Float(
        string="Product packaging qty (Demand)",
        compute="_compute_product_packaging_qty",
        precompute=False,
    )
    done_product_packaging_qty = fields.Float(
        string="Product packaging qty (Done)",
        compute="_compute_product_packaging_qty",
        precompute=False,
    )
    boxes_sacks = fields.Integer(string="Boxes/Sacks", compute="_compute_bosex_sacs")
    product_packaging_qty = fields.Float(
        string="Packaging Quantity", compute="_compute_packaging_qty", store=True
    )
    palet_qty = fields.Float(
        string="Contained Palet Quantity",
        digits="Product Unit of Measure",
        compute="_compute_palet_qty",
        store=True,
    )

    @api.depends("move_line_ids", "move_line_ids.product_packaging_qty")
    def _compute_packaging_qty(self):
        for move in self:
            if move.move_line_ids:
                move.product_packaging_qty = sum(
                    move.move_line_ids.mapped("product_packaging_qty")
                )
            elif move.sale_line_id:
                move.product_packaging_qty = move.sale_line_id.product_packaging_qty

    @api.depends("move_line_ids", "move_line_ids.palet_qty")
    def _compute_palet_qty(self):
        for move in self:
            if move.move_line_ids:
                move.palet_qty = sum(move.move_line_ids.mapped("palet_qty"))
            elif move.sale_line_id:
                move.palet_qty = move.sale_line_id.palet_qty
