# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    @api.model
    def _prepare_stock_move_vals(self):
        self.ensure_one()
        values = super()._prepare_stock_move_vals()
        values["name"] = self.product_id.display_name
        return values
