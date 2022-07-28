# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    standard_price = fields.Float(string="Cost")
    amount = fields.Float(string="Amount")

    @api.onchange("product_id")
    def _onchange_product_id(self):
        if self.product_id and self.product_id.standard_price:
            self.standard_price = self.product_id.standard_price

    @api.onchange("standard_price", "quantity_done")
    def onchange_standard_price(self):
        if self.standard_price and self.quantity_done:
            self.amount = self.standard_price * self.quantity_done
