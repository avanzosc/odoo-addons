# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common
from openerp import fields
from dateutil.relativedelta import relativedelta


class TestStockLotLifespan(common.TransactionCase):

    def setUp(self):
        super(TestStockLotLifespan, self).setUp()
        self.config_model = self.env['stock.config.settings']
        self.lot_model = self.env['stock.production.lot']
        self.product = self.env.ref('product.product_product_3')
        self.now = fields.Date.from_string(fields.Date.today())
        self.last_year = self.now - relativedelta(years=1)
        self.next_year = self.now + relativedelta(years=1)
        lot_vals = {
            'name': 'Testing Lot',
            'product_id': self.product.id,
        }
        self.lot = self.lot_model.create(lot_vals)

    def test_configuration_fields(self):
        config = self.config_model.create({})
        vals = config.get_default_stock_lot_percentage([])
        self.assertEqual(vals.get('stock_lot_percentage1', 0), 50)
        self.assertEqual(vals.get('stock_lot_percentage2', 0), 75)
        self.assertEqual(vals.get('stock_lot_percentage3', 0), 90)
        config = self.config_model.create({})
        config.get_default_stock_lot_percentage([])
        config.stock_lot_percentage1 = 20
        config.stock_lot_percentage2 = 40
        config.execute()
        vals = config.get_default_stock_lot_percentage([])
        self.assertEqual(vals.get('stock_lot_percentage1', 0), 20)
        self.assertEqual(vals.get('stock_lot_percentage2', 0), 40)
        self.assertEqual(vals.get('stock_lot_percentage3', 0), 90)

    def test_lot_dates(self):
        self.lot.mrp_date = self.last_year
        self.lot.onchange_mrp_life_date()
        self.assertFalse(self.lot.alert_date)
        self.assertFalse(self.lot.removal_date)
        self.assertFalse(self.lot.use_date)
        self.lot.life_date = self.next_year
        self.lot.onchange_mrp_life_date()
        lifespan = (self.next_year - self.last_year).days
        alert_date = self.last_year + relativedelta(days=(lifespan * 0.5))
        removal_date = self.last_year + relativedelta(days=(lifespan * 0.75))
        use_date = self.last_year + relativedelta(days=(lifespan * 0.9))
        self.assertEqual(fields.Date.from_string(self.lot.alert_date),
                         alert_date)
        self.assertEqual(fields.Date.from_string(self.lot.removal_date),
                         removal_date)
        self.assertEqual(fields.Date.from_string(self.lot.use_date), use_date)
        limit1 = self.lot_model.get_lots_by_limit(self.lot.alert_date, 1)
        self.assertTrue(self.lot.name in limit1)
        limit2 = self.lot_model.get_lots_by_limit(self.lot.alert_date, 2)
        self.assertFalse(self.lot.name in limit2)
        limit3 = self.lot_model.get_lots_by_limit(self.lot.alert_date, 3)
        self.assertFalse(self.lot.name in limit3)
        limit4 = self.lot_model.get_lots_by_limit(self.lot.removal_date, 2)
        self.assertTrue(self.lot.name in limit4)
        limit5 = self.lot_model.get_lots_by_limit(self.lot.use_date, 3)
        self.assertTrue(self.lot.name in limit5)
        self.assertEqual(self.lot.lifespan_progress, 50)

    def test_lot_qtys(self):
        self.assertEquals(self.lot_model.search_count([
                          ('product_id', '=', self.product.id)]), 1)
        lots = self.lot_model.search([
            ('qty_available', '=', self.product.qty_available)])
        self.assertIn(self.lot, lots)
        self.assertEquals(self.lot.qty_available, self.product.qty_available)
        lots = self.lot_model.search([
            ('virtual_available', '=', self.product.virtual_available)])
        self.assertIn(self.lot, lots)
        self.assertEquals(
            self.lot.virtual_available, self.product.virtual_available)
        lots = self.lot_model.search([
            ('incoming_qty', '=', self.product.incoming_qty)])
        self.assertIn(self.lot, lots)
        self.assertEquals(self.lot.incoming_qty, self.product.incoming_qty)
        lots = self.lot_model.search([
            ('outgoing_qty', '=', self.product.outgoing_qty)])
        self.assertIn(self.lot, lots)
        self.assertEquals(self.lot.outgoing_qty, self.product.outgoing_qty)

    def test_send_email(self):
        self.lot_model.send_mail('ainaragaldona@avanzosc.es')
        mails = self.env['mail.mail'].search([('email_to', '=',
                                               'ainaragaldona@avanzosc.es')])
        self.assertTrue(mails and mails[0].state == 'sent')
