# Copyright 2022 Leire Martinez de Santos - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, models


class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.multi
    def update_stock_movement_qty_desc(self, new_quant, qty_delivered):
        self.ensure_one()
        if self.state not in ('done', 'cancel') and new_quant < self.product_uom_qty:
            if self.product_uom_qty < qty_delivered:
                updated_qty = qty_delivered
            else:
                updated_qty = new_quant - qty_delivered
            self.product_uom_qty = updated_qty

