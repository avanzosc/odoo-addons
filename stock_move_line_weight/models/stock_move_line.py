# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    weight = fields.Float(
        string="Weight",
        digits="Stock Weight",
        store=True,
        copy=False,
        compute="_compute_weight",
    )

    @api.depends("qty_done", "product_id", "product_id.weight")
    def _compute_weight(self):
        for line in self:
            weight = 0
            if line.qty_done and line.product_id:
                weight = line.qty_done * line.product_id.weight
            line.weight = weight
