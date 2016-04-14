# -*- coding: utf-8 -*-
# © 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common


class TestLostObject(common.TransactionCase):

    def setUp(self):
        super(TestLostObject, self).setUp()
        self.ir_sequence_model = self.env['ir.sequence']
        self.lost_object_sequence = self.browse_ref('lost_object.lost_object')
        self.get_model = self.env['get.object.wiz']
        self.give_model = self.env['give.object.wiz']
        self.move_model = self.env['move.object.wiz']

    def test_get_object(self):
        sequence = self._get_next_code()
        get_wiz = self.get_model.create({
            'description': 'Blue jacket',
            'location_id': self.ref('stock.stock_location_14')
            })
        product = self.env.ref('lost_object.product_lost_object')
        self.assertEqual(product, get_wiz.product_id)
        self.assertEqual(sequence, get_wiz.sequence)
        get_wiz.confirm_get_object_lost()
        quant = self.env['stock.quant'].search([
            ('lot_id', '=', sequence)])
        self.assertEqual(quant.location_id, get_wiz.location_id)
        get_move_wiz = self.move_model.create({
            'lot_id': quant.lot_id.id,
            'location_id': self.ref('stock.stock_location_3')
            })
        get_move_wiz.confirm_move_object()
        self.assertEqual(quant.location_id, get_move_wiz.location_id)
        get_give_wiz = self.give_model.create({
            'lot_id': quant.lot_id.id,
            })
        self.assertEqual(
            get_give_wiz.location_id.id,
            self.ref('lost_object.stock_location_virtual_customer'))
        get_give_wiz.confirm_give_object()

    def _get_next_code(self):
        d = self.ir_sequence_model._interpolation_dict()
        prefix = self.ir_sequence_model._interpolate(
            self.lost_object_sequence.prefix, d)
        suffix = self.ir_sequence_model._interpolate(
            self.lost_object_sequence.suffix, d)
        name = (prefix + ('%%0%sd' % self.lost_object_sequence.padding %
                          self.lost_object_sequence.number_next_actual) +
                suffix)
        return name
