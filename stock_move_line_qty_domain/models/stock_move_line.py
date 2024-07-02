# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    @api.onchange("product_id", "lot_id", "location_id", "qty_done")
    def _onchange_qty_done(self):
        result = super()._onchange_qty_done()
        stock_qty = False
        if (
            self.product_id
            and self.product_id.tracking == "none"
            and (self.location_id)
            and (self.location_id.usage == "internal")
        ):
            stock_qty = (
                self.env["stock.quant"]
                .search(
                    [
                        ("product_id", "=", self.product_id.id),
                        ("location_id", "=", self.location_id.id),
                    ]
                )
                .quantity
            )
        elif (
            self.product_id
            and self.product_id.tracking != "none"
            and (self.lot_id)
            and self.location_id
            and (self.location_id.usage == "internal")
        ):
            stock_qty = (
                self.env["stock.quant"]
                .search(
                    [
                        ("product_id", "=", self.product_id.id),
                        ("location_id", "=", self.location_id.id),
                        ("lot_id", "=", self.lot_id.id),
                    ]
                )
                .quantity
            )
        if stock_qty and stock_qty < self.qty_done:
            self.qty_done = stock_qty
        return result
