# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common
from dateutil.relativedelta import relativedelta
from datetime import datetime


class TestPurchaseOrderSplit(common.TransactionCase):

    def setUp(self):
        super(TestPurchaseOrderSplit, self).setUp()
        self.purchase_model = self.env['purchase.order']
        self.wiz_split_model = self.env['wiz.purchase.order.split']
        product = self.env.ref('product.product_product_4')
        vals = self.purchase_model. onchange_partner_id(
            self.ref('base.res_partner_1'))
        value = vals.get('value')
        purchase_vals = {
            'partner_id': self.ref('base.res_partner_1'),
            'origin': 'probe order split',
            'pricelist_id': value.get('pricelist_id'),
            'payment_term_id': value.get('payment_term_id'),
            'fiscal_position': value.get('fiscal_position'),
            'location_id': self.ref('stock.stock_location_locations_partner'),
            'state': 'draft'}
        purchase_line_vals = {
            'product_id': product.id,
            'name': product.name,
            'product_qty': 100,
            'price_unit': 5,
            'date_planned': '2016-02-25'}
        purchase_vals['order_line'] = [(0, 0, purchase_line_vals)]
        self.purchase = self.purchase_model.create(purchase_vals)

    def test_purchase_order_split(self):
        wiz_vals = {'parts': 5,
                    'from_date': '2016-03-30',
                    'each_month': 2}
        wiz = self.wiz_split_model.create(wiz_vals)
        wiz.with_context(
            {'active_ids': [self.purchase.id]}).action_split_purchase_order()
        first_date = datetime.strptime('2016-03-30', '%Y-%m-%d').date()
        month_count = 5
        while month_count > 1:
            next_date = first_date + relativedelta(months=2)
            cond = [('partner_id', '=', self.ref('base.res_partner_1')),
                    ('minimum_planned_date', '=', next_date)]
            purchase = self.purchase_model.search(cond, limit=1)
            self.assertEqual(
                len(purchase), 1, 'Purchases no generated')
            first_date = datetime.strptime(
                str(next_date), '%Y-%m-%d').date()
            month_count -= 1
        next_date = first_date + relativedelta(months=2)
        cond = [('partner_id', '=', self.ref('base.res_partner_1')),
                ('minimum_planned_date', '=', next_date)]
        purchase = self.purchase_model.search(cond, limit=1)
        self.assertEqual(
            len(purchase), 1, 'Purchases no generated')
