# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    def _default_standard_price(self):
        result = 0
        if self.sale_line_id and self.sale_line_id.price_unit:
            result = self.sale_line_id.price_unit
        elif self.purchase_line_id and self.purchase_line_id.price_unit:
            result = self.purchase_line_id.price_unit
        elif self.product_id:
            result = self.product_id.standard_price
        return result

    standard_price = fields.Float(string="Cost", default=_default_standard_price)
    amount = fields.Float(string="Amount")

    @api.onchange("sale_line_id")
    def _onchange_sale_line_id(self):
        if self.sale_line_id:
            self.standard_price = self.sale_line_id.price_unit
            self.onchange_standard_price()

    @api.onchange("purchase_line_id")
    def _onchange_purchase_line_id(self):
        if self.purchase_line_id:
            self.standard_price = self.purchase_line_id.price_unit
            for line in self.move_line_ids:
                line.standard_price = self.standard_price
                line.onchange_standard_price()
            self.onchange_standard_price()

    @api.onchange("product_id")
    def _onchange_product_id(self):
        if self.sale_line_id and self.sale_line_id.price_unit:
            self.standard_price = self.sale_line_id.price_unit
        elif self.purchase_line_id and self.purchase_line_id.price_unit:
            self.standard_price = self.purchase_line_id.price_unit
        elif self.product_id and self.product_id.standard_price:
            self.standard_price = self.product_id.standard_price

    @api.onchange("standard_price", "quantity_done")
    def onchange_standard_price(self):
        if self.standard_price:
            self.amount = self.standard_price * self.quantity_done

    @api.depends(
        "move_line_ids.qty_done",
        "move_line_ids.product_uom_id",
        "move_line_nosuggest_ids.qty_done",
        "picking_type_id",
    )
    def _quantity_done_compute(self):
        result = super()._quantity_done_compute()
        for line in self:
            line.onchange_standard_price()
        return result
