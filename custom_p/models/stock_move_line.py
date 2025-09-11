# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    @api.model
    def _prepare_stock_move_vals(self):
        result = super()._prepare_stock_move_vals()
        result.update(
            {
                "name": self.product_id.display_name,
            }
        )
        return result
