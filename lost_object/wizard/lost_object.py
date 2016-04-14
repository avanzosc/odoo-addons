# -*- coding: utf-8 -*-
# © 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, models, fields


class GetObjectWiz(models.TransientModel):
    _name = 'get.object.wiz'

    @api.multi
    def _default_sequence(self):
        return self.env['ir.sequence'].next_by_code('lost.object')

    @api.multi
    def _default_product_id(self):
        product = self.env.ref('lost_object.product_lost_object', False)
        return product

    sequence = fields.Char(
        string='Sequence', default=_default_sequence)
    product_id = fields.Many2one(
        comodel_name='product.product', string='Product',
        default=_default_product_id)
    description = fields.Char()
    location_id = fields.Many2one(
        comodel_name='stock.location', domain=[('usage', '=', 'internal')])

    @api.multi
    def confirm_get_object_lost(self):
        location = self.env.ref('lost_object.stock_location_lost')
        lot = self.env['stock.production.lot'].create({
            'name': self.sequence,
            'product_id': self.product_id.id,
            'ref': self.description})
        move = self.env['stock.move'].create({
            'product_uom_qty': 1,
            'product_id': self.product_id.id,
            'location_dest_id': self.location_id.id,
            'name': self.product_id.name,
            'product_uom': self.product_id.uom_id.id,
            'location_id': location.id,
            })
        move.action_done()
        quant = self.env['stock.quant'].search([
            ('history_ids', 'in', move.id)])
        quant.lot_id = lot


class MoveObjectWiz(models.TransientModel):
    _name = 'move.object.wiz'

    @api.multi
    def confirm_move_object(self):
        quant = self.env['stock.quant'].search([
            ('lot_id', '=', self.lot_id.id)])
        move = self.env['stock.move'].create({
            'product_uom_qty': 1,
            'product_id': self.lot_id.product_id.id,
            'location_dest_id': self.location_id.id,
            'name': self.lot_id.product_id.name,
            'product_uom': self.lot_id.product_id.uom_id.id,
            'location_id': quant.location_id.id
            })
        move.action_done()

    lot_id = fields.Many2one(
        comodel_name='stock.production.lot', string='Lot',
        domain=[('quant_ids.location_id.usage', '=', 'internal')])
    location_id = fields.Many2one(
        comodel_name='stock.location', domain=[('usage', '=', 'internal')])


class GiveObjectWiz(models.TransientModel):
    _name = 'give.object.wiz'

    def _default_location_id(self):
        return self.env.ref('lost_object.stock_location_virtual_customer')

    @api.multi
    def confirm_give_object(self):
        quant = self.env['stock.quant'].search([
            ('lot_id', '=', self.lot_id.id)])
        move = self.env['stock.move'].create({
            'product_uom_qty': 1,
            'product_id': self.lot_id.product_id.id,
            'location_dest_id': self.location_id.id,
            'name': self.lot_id.product_id.name,
            'product_uom': self.lot_id.product_id.uom_id.id,
            'location_id': quant.location_id.id
            })
        move.action_done()

    lot_id = fields.Many2one(
        comodel_name='stock.production.lot', string='Lot',
        domain=[('quant_ids.location_id.usage', '=', 'internal')])
    location_id = fields.Many2one(
        comodel_name='stock.location', default=_default_location_id)
