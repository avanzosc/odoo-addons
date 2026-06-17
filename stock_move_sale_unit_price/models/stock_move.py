# Copyright 2020 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    @api.depends("sale_line_id.price_unit", "sale_line_id.discount", "quantity")
    def _compute_pvp_price_unit(self):
        for move in self:
            pvp_price_unit = 0
            if move.sale_line_id:
                pvp_price_unit = move.sale_line_id.price_unit * (
                    1 - move.sale_line_id.discount / 100
                )
            move.pvp_price_unit = pvp_price_unit
            move.subtotal_pvp_price_unit = pvp_price_unit * move.quantity

    pvp_price_unit = fields.Float(
        string="Sale unit price", compute="_compute_pvp_price_unit", store=True
    )
    subtotal_pvp_price_unit = fields.Float(
        string="Subtotal sale unit price", store=True, compute="_compute_pvp_price_unit"
    )
