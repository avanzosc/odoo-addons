# -*- coding: utf-8 -*-
# © 2016 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import _, api, exceptions, fields, models


class CaptureMove(models.TransientModel):
    _name = 'capture.move'
    _description = 'Capture moves'

    def _default_warehouse_id(self):
        warehouse_obj = self.env['stock.warehouse']
        warehouse = warehouse_obj.search([])
        if len(warehouse) == 1:
            return warehouse.id
        return self.env['stock.warehouse']

    warehouse_id = fields.Many2one(
        comodel_name='stock.warehouse', string='Warehouse',
        default=_default_warehouse_id)
    product_ids = fields.One2many(
        comodel_name='product.move', inverse_name='move_id', string='Products')

    @api.multi
    def action_confirm_move(self):
        picking_obj = self.env['stock.picking']
        move_lines = []
        if not self.warehouse_id.cap_type_id:
            raise exceptions.Warning(
                _('You need to select a capture picking for the warehouse!'))
        for line in self.product_ids:
            move_lines += [(0, 0, {
                'product_id': line.product_id.id,
                'product_uom': line.product_id.uom_id.id,
                'product_uom_qty': line.quantity,
                'location_id': line.location_id.id,
                'location_dest_id': line.location_dest_id.id,
                'name': line.product_id.name,
            })]
        picking = picking_obj.create({
            'picking_type_id': self.warehouse_id.cap_type_id.id,
            'move_lines': move_lines,
        })
        picking.action_confirm()
        picking.action_assign()
        picking.force_assign()
        wiz_view = picking.do_enter_transfer_details()
        wiz = self.env['stock.transfer_details'].browse(wiz_view['res_id'])
        wiz.with_context(
            active_id=wiz_view['context']['active_id']).do_detailed_transfer()
        return {
            'name': _('Picking'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'stock.picking',
            'view_id': self.env.ref('stock.view_picking_form').id,
            'type': 'ir.actions.act_window',
            'target': 'current',
            'readonly': True,
            'res_id': picking.id,
            'context': self.env.context
            }


class ProductMove(models.TransientModel):
    _name = 'product.move'
    _description = 'Product moves'

    quantity = fields.Integer(string='Quantity')
    product_id = fields.Many2one(
        comodel_name='product.product', string='Product')
    location_id = fields.Many2one(
        comodel_name='stock.location', string='Location')
    location_dest_id = fields.Many2one(
        comodel_name='stock.location', string='Destination Location')
    move_id = fields.Many2one(comodel_name='capture.move')
