# Copyright 2020 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, api


class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.multi
    @api.depends('pvp_price_unit', 'quantity_done')
    def _compute_pvp_price_unit(self):
        for move in self:
            move.subtotal_pvp_price_unit = (
                move.pvp_price_unit * move.quantity_done)

    pvp_price_unit = fields.Float(
        string='Sale unit price', related='sale_line_id.price_reduce',
        store=True)
    subtotal_pvp_price_unit = fields.Float(
        string='Subtotal sale unit price', store=True,
        compute='_compute_pvp_price_unit')
