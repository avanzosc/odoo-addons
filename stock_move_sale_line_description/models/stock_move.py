# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class StockMove(models.Model):
    _inherit = "stock.move"

    @api.onchange("sale_line_id")
    def compute_stock_move_description(self):
        for record in self:
            if record.sale_line_id:
                record.name = record.sale_line_id.name

    @api.model
    def create(self, vals):
        res = super().create(vals)
        if res.sale_line_id:
            res.compute_stock_move_description()
        return res
