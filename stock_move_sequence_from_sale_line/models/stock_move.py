# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    sequence = fields.Integer(
        compute="_compute_sequence", store=True, copy=False, readonly=True
    )

    @api.depends("sale_line_id", "sale_line_id.sequence")
    def _compute_sequence(self):
        for move in self:
            sequence = 0
            if move.sale_line_id:
                sequence = move.sale_line_id.sequence
            move.sequence = sequence
