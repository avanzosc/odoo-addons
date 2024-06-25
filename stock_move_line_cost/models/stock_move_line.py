# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    def _default_standard_price(self):
        result = 0
        if self.move_id.sale_line_id:
            result = self.move_id.sale_line_id.price_unit
        elif self.move_id.purchase_line_id:
            result = self.move_id.purchase_line_id.price_unit
        elif self.product_id:
            result = self.product_id.standard_price
        return result

    standard_price = fields.Float(string="Cost", default=_default_standard_price)
    amount = fields.Float(string="Amount")

    @api.onchange("product_id", "product_uom_id")
    def _onchange_product_id(self):
        res = super()._onchange_product_id()
        if self.move_id.sale_line_id:
            self.standard_price = self.move_id.sale_line_id.price_unit
        elif self.move_id.purchase_line_id:
            self.standard_price = self.move_id.purchase_line_id.price_unit
        elif self.product_id and self.product_id.standard_price:
            self.standard_price = self.product_id.standard_price
        return res

    @api.onchange("standard_price", "qty_done")
    def onchange_standard_price(self):
        if self.standard_price:
            self.move_id.standard_price = self.standard_price
            self.move_id.onchange_standard_price()
            self.amount = self.standard_price * self.qty_done

    @api.onchange("lot_id")
    def onchange_lot_id(self):
        if not self.standard_price:
            self._onchange_product_id()
            self.onchange_standard_price()
