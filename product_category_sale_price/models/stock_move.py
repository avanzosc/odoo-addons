# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, models


class StockMove(models.Model):
    _inherit = "stock.move"

    def product_price_update_before_done(self, forced_qty=None):
        return super(
            StockMove, self.with_context(update_base_cost=True)
        ).product_price_update_before_done(forced_qty=forced_qty)
