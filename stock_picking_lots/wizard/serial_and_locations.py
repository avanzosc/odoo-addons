# Copyright (C) 2013 Obertix Free Software Solutions (<http://obertix.net>).
#                    cubells <info@obertix.net>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
import odoo.addons.decimal_precision as dp


class StockSerialPicking(models.TransientModel):
    _name = "stock.serial.picking"

    move_id = fields.Many2one(comodel_name='stock.move', string='Line')
    product_id = fields.Many2one('product.product', string="Product"),
    quantity = fields.Float(
            string="Cantidad",
            digits=dp.get_precision('Product Unit of Measure'))
    prodlot_id = fields.Char(string='Lote')
    location_dest_id = fields.Many2one(
        comodel_name='stock.location', string='Ubicación Destino',
        domain=[('usage', '<>', 'view')])
    state = fields.Selection(
        selection=[('selection', 'selection'),
                   ('intro', 'intro')], string='State', default='intro')

    @api.model
    def default_get(self, fields):
        context = self.env.context or {}
        picking_obj = self.pool['stock.picking']
        move_obj = self.pool['stock.move']
        res = super(StockSerialPicking, self).default_get(fields)
        picking_ids = context.get('active_ids', [])
        active_model = context.get('active_model')

        if not picking_ids or len(picking_ids) != 1:
            return res
        assert active_model in ('stock.picking', 'stock.picking.in',
                                'stock.picking.out'), 'Bad context propagation'
        if 'move_id' in fields:
            picking = picking_obj.browse(picking_ids[:1])
            move = move_obj.search([
                ('state', 'not in', ('done', 'cancel')),
                ('picking_id', '=', picking.id)
            ], context=context, order='product_id', limit=1)
            if move:
                res.update({
                    'move_id': move.id,
                    'product_id': move.product_id.id,
                    'quantity': move.product_qty,
                    'location_dest_id': move.location_dest_id.id,
                })
        return res

    def next_serial(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        assert len(ids) == 1, 'Partial picking processing may only be done one at a time.'
        stock_picking = self.pool['stock.picking']
        stock_move = self.pool['stock.move']
        uom_obj = self.pool['product.uom']
        partial = self.browse(cr, uid, ids[0], context=context)
        partial_data = {
            'delivery_date': partial.date
        }
        picking_type = partial.picking_id.type
        for wizard_line in partial.move_ids:
            pass
        return {'type': 'ir.actions.act_window_close'}

