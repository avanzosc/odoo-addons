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
    product_packaging_qty = fields.Float(
        string="Packaging Quantity", compute="_compute_packaging_qty", store=True
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
