# -*- coding: utf-8 -*-
# © 2016 Ainara Galdona - AvanzOSC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api, _
from openerp.tools import float_is_zero


class MrpProduction(models.Model):

    _inherit = 'mrp.production'

    inverse = fields.Boolean(string="Inverse")

    @api.multi
    def _make_inverse(self, move_id):
        move = self.env['stock.move'].browse(move_id)
        dest_location = move.location_id.id
        src_location = move.location_dest_id.id
        raw_production = move.production_id.id or False
        production = move.raw_material_production_id.id or False
        move.write({
            'raw_material_production_id': raw_production,
            'production_id': production,
            'location_id': src_location,
            'location_dest_id': dest_location
        })

    @api.multi
    def bom_id_change(self, bom_id):
        res = super(MrpProduction, self).bom_id_change(bom_id)
        if bom_id:
            bom = self.env['mrp.bom'].browse(bom_id)
            res['value']['inverse'] = bom.inverse
        return res

    @api.model
    def _make_production_consume_line(self, line):
        move = super(MrpProduction, self)._make_production_consume_line(line)
        if line.production_id.inverse:
            self._make_inverse(move)
        return move

    @api.model
    def _make_production_produce_line(self, production):
        move = super(MrpProduction, self)._make_production_produce_line(
            production)
        if production.inverse:
            self._make_inverse(move)
        return move

    @api.multi
    def action_inverse_produce(self, wiz):
        self.ensure_one()
        precision = self.env['decimal.precision'].precision_get(
            'Product Unit of Measure')
        if wiz.mode == 'consume_produce':
            produce_lines = []
            for cons in wiz.consume_lines:
                produce_lines.append(
                    {'product_id': cons.product_id.id,
                     'lot_id': cons.lot_id.id,
                     'product_qty': cons.product_qty})
            for produce in produce_lines:
                remaining_qty = produce['product_qty']
                for produce_material_line in \
                        (self.move_created_ids.filtered(
                         lambda x: x.product_id.id == produce['product_id'])):
                    if remaining_qty <= 0:
                        break
                    qty = min(remaining_qty, produce_material_line.product_qty)
                    produce_material_line.action_consume(
                        qty, location_id=produce_material_line.location_id.id,
                        restrict_lot_id=produce['lot_id'])
                    remaining_qty -= qty
                    if not float_is_zero(remaining_qty,
                                         precision_digits=precision):
                        extra_move_id = produce_material_line.copy()
                        extra_move_id.write({'product_uom_qty': remaining_qty,
                                             'production_id': self.id})
                        extra_move_id.action_confirm()
                        extra_move_id.action_done()
        if wiz.mode in ['consume', 'consume_produce']:
            remaining_qty = wiz.product_qty
            for raw_material_line in \
                    self.move_lines.filtered(lambda x: x.product_id ==
                                             wiz.product_id):
                if remaining_qty <= 0:
                    break
                consumed_qty = min(remaining_qty,
                                   raw_material_line.product_qty)
                raw_material_line.action_consume(
                    consumed_qty, raw_material_line.location_id.id)
                remaining_qty -= consumed_qty
            if not float_is_zero(remaining_qty, precision_digits=precision):
                product = wiz.product_id
                extra_move_id = self._make_consume_line_from_data(
                    self, product, product.uom_id.id, remaining_qty,
                    False, 0)
                self._make_inverse(extra_move_id)
                extra_move = self.env['stock.move'].browse(extra_move_id)
                extra_move.action_done()
        body = "{} {}".format(self._description, _("produced"))
        self.message_post(body=body)
        if not self.move_created_ids and self.move_lines:
            self.move_lines.action_cancel()
        self.signal_workflow('button_produce_done')
        return True
