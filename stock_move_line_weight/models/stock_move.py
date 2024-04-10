# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    weight = fields.Float(
        string="Weight",
        digits="Stock Weight",
        store=True,
        copy=False,
        compute="_compute_weight",
    )

    @api.depends("quantity_done", "product_id", "product_id.weight")
    def _compute_weight(self):
        for move in self:
            weight = 0
            if move.quantity_done and move.product_id:
                weight = move.quantity_done * move.product_id.weight
            move.weight = weight
