# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class StockMove(models.Model):
    _inherit = "stock.move"

    @api.depends(
        "sale_line_id",
        "sale_line_id.sequence",
        "purchase_line_id",
        "purchase_line_id.sequence",
    )
    def _compute_sequence(self):
        for move in self:
            sequence = 0
            if move.sale_line_id:
                sequence = move.sale_line_id.sequence
            if move.purchase_line_id:
                sequence = move.purchase_line_id.sequence
            move.sequence = sequence
