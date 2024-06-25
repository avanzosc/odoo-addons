# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    sale_price_unit = fields.Float(
        string="Sale Unit Price",
        digits="Product Price",
        related="sale_line_id.price_unit",
        store=True,
        copy=False,
    )
    sale_price_subtotal = fields.Float(
        string="Sale Subtotal",
        digits="Product Price",
        store=True,
        copy=False,
        compute="_compute_sale_price_subtotal",
    )

    @api.depends("state", "sale_price_unit", "is_done")
    def _compute_sale_price_subtotal(self):
        for move in self:
            sale_price_subtotal = 0
            if move.sale_price_unit > 0:
                if move.state == "done":
                    sale_price_subtotal = move.quantity_done * move.sale_price_unit
                if move.state not in ("done", "cancel"):
                    sale_price_subtotal = (
                        move.reserved_availability * move.sale_price_unit
                    )
            move.sale_price_subtotal = sale_price_subtotal
