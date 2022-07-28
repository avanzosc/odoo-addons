# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    standard_price = fields.Float(string="Cost")
    amount = fields.Float(string="Amount")

    @api.onchange('product_id', 'product_uom_id')
    def _onchange_product_id(self):
        res = super()._onchange_product_id()
        if self.product_id and self.product_id.standard_price:
            self.standard_price = self.product_id.standard_price
        return res

    @api.onchange("standard_price", "qty_done")
    def onchange_standard_price(self):
        if self.standard_price and self.qty_done:
            self.amount = self.standard_price * self.qty_done
