# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    price_unit_cost = fields.Float(
        string="Cost Unit Price",
        digits="Product Price",
        store=True,
        copy=False,
        compute="_compute_price_unit_cost",
    )
    cost = fields.Float(
        string="Cost",
        digits="Product Price",
        store=True,
        copy=False,
        compute="_compute_price_unit_cost",
    )

    @api.depends("quantity_done", "move_line_ids", "move_line_ids.cost")
    def _compute_price_unit_cost(self):
        for move in self:
            cost = sum(move.move_line_ids.mapped("cost"))
            move.cost = cost
            if cost and move.quantity_done:
                move.price_unit_cost = cost / move.quantity_done
            else:
                move.price_unit_cost = 0
