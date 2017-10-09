# -*- coding: utf-8 -*-
# (c) 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models, api
import openerp.addons.decimal_precision as dp


class WizGenerateInitialMove(models.TransientModel):
    _name = 'wiz.generate.initial.move'

    picking_id = fields.Many2one(
        comodel_name='stock.picking', string='Picking')
    stock_picking_type = fields.Many2one(
        comodel_name='stock.picking.type', string='Picking type')
    lines = fields.One2many(
        comodel_name='wiz.generate.initial.move.line',
        inverse_name='wiz_id', string='Products without move')

    @api.model
    def default_get(self, var_fields):
        product_obj = self.env['product.product']
        res = super(WizGenerateInitialMove, self).default_get(var_fields)
        vals = []
        picking_type = self.env['stock.picking.type'].search(
            [('code', '=', 'incoming')], limit=1)
        for product in product_obj.browse(self.env.context.get('active_ids')):
            vals.append({'product_id': product.id,
                         'product_uom_qty': 1.0})
        res.update({'stock_picking_type': picking_type.id, 'lines': vals})
        return res

    @api.multi
    def button_generate_moves(self):
        self.ensure_one()
        lines = self.lines.filtered(lambda x: x.product_uom_qty > 0)
        picking_type = self.picking_id.picking_type_id
        for line in lines:
            vals = {'name': line.product_id.name,
                    'picking_id': self.picking_id.id,
                    'picking_type_id': picking_type.id,
                    'origin': self.picking_id.name,
                    'product_id': line.product_id.id,
                    'product_uom': line.product_id.uom_id.id,
                    'price_unit': line.product_id.standard_price,
                    'location_id': picking_type.default_location_src_id.id,
                    'location_dest_id':
                    picking_type.default_location_dest_id.id}
            self.env['stock.move'].create(vals)
        return {'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'stock.picking',
                'type': 'ir.actions.act_window',
                'domain': "[('id', '=', " + str(self.picking_id.id) + ")]",
                'context': self.env.context}


class WizGenerateInitialMoveLine(models.TransientModel):
    _name = 'wiz.generate.initial.move.line'

    wiz_id = fields.Many2one(
        comodel_name='wiz.generate.initial.move', string='Wizard')
    product_id = fields.Many2one(
        comodel_name='product.product', string='Product')
    product_uom_qty = fields.Float(
        string='Quantity',
        digits_compute=dp.get_precision('Product Unit of Measure'))
