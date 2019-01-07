# -*- coding: utf-8 -*-
# Copyright © 2018 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common
from openerp import exceptions


class TestStockProductionLotHistory(common.TransactionCase):

    def setUp(self):
        super(TestStockProductionLotHistory, self).setUp()
        state_obj = self.env['stock.production.lot.status']
        self.state1 = self.env.ref(
            'stock_production_lot_history.first_lot_status')
        self.state2 = state_obj.create({'name': 'State-2'})
        self.state3 = state_obj.create({'name': 'State-3'})
        product = self.env['product.product'].search([], limit=1)
        lot_vals = ({'name': 'Lot for test lot history',
                     'product_id': product.id})
        self.lot = self.env['stock.production.lot'].create(lot_vals)

    def test_stock_production_lot_history(self):
        self.assertEqual(len(self.lot.historical_states_ids), 0,
                         'Bad lot state(1)')
        wiz_vals = {'lot_status_id': self.state2.id,
                    'reason': 'This is the reason'}
        wiz = self.env['wiz.change.lot.state'].create(wiz_vals)
        wiz.with_context(active_ids=[self.lot.id]).change_lot_state()
        self.assertEqual(self.lot.lot_status_id, self.state2,
                         'Bad lot state(2)')
        self.assertEqual(len(self.lot.historical_states_ids), 1,
                         'Bad lot state(2-1)')
        wiz_vals = {'lot_status_id': self.state3.id,
                    'reason': 'This is the reason2'}
        wiz = self.env['wiz.change.lot.state'].create(wiz_vals)
        wiz.with_context(active_ids=[self.lot.id]).change_lot_state()
        self.assertEqual(self.lot.lot_status_id, self.state3,
                         'Bad lot state(3)')
        self.assertEqual(len(self.lot.historical_states_ids), 2,
                         'Bad lot state(3-1)')
        with self.assertRaises(exceptions.Warning):
            self.state1.unlink()
