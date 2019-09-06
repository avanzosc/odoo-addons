# -*- coding: utf-8 -*-
# Copyright © 2019 Oihana Larrañaga - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models, api


class StockMove(models.Model):
    _inherit = 'stock.move'

    price_subtotal = fields.Float(
        string='Price subtotal', compute='_compute_price_subtotal',
        store=True)
    reserved = fields.Float(
        string='Reserved', related='product_id.reserved')
    unreserved = fields.Float(
        string='Unreserved', compute='_compute_unreserved')

    @api.depends('price_unit', 'product_uom_qty')
    def _compute_price_subtotal(self):
        for move in self.filtered(lambda o: o.price_unit and
                                  o.product_uom_qty):
            move.price_subtotal = (
                move.price_unit * move.product_uom_qty)

    @api.depends('reserved', 'product_id.virtual_available')
    def _compute_unreserved(self):
        for move in self:
            move.unreserved = (move.product_id.virtual_available -
                               move.reserved)


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    price_total = fields.Float(
        string='Price total', compute='_compute_price_total')

    def _compute_price_total(self):
        for picking in self:
            picking.price_total += sum(
                picking.move_lines.mapped('price_subtotal'))
