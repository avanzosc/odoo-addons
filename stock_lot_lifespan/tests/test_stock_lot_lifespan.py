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
