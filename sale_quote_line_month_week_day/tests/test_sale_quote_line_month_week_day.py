# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp.tests.common import TransactionCase


class TestSaleQuoteLineMonthWeekDay(TransactionCase):

    def setUp(self):
        super(TestSaleQuoteLineMonthWeekDay, self).setUp()
        self.sale_model = self.env['sale.order']
        self.line_template = self.env.ref(
            'website_quote.website_sale_order_line_1')
        self.line_template.write({'january': True,
                                  'december': True,
                                  'week1': True,
                                  'week5': True,
                                  'monday': True,
                                  'sunday': True})
        sale_vals = {
            'partner_id': self.ref('base.res_partner_1'),
            'partner_shipping_id': self.ref('base.res_partner_1'),
            'partner_invoice_id': self.ref('base.res_partner_1'),
            'pricelist_id': self.env.ref('product.list0').id,
            'template_id': self.line_template.quote_id.id}
        self.sale_order = self.sale_model.create(sale_vals)

    def test_sale_quote_line_month_week_day(self):
        res = self.sale_order.onchange_template_id(
            self.line_template.quote_id.id,
            partner=self.sale_order.partner_id.id)
        order_lines = res.get('value')['order_line']
        for line in order_lines:
            if len(line) > 1:
                dic = line[2]
                product_id = dic.get('product_id', False)
                if product_id == self.line_template.product_id.id:
                    january = dic.get('january', False)
                    december = dic.get('december', False)
                    week1 = dic.get('week1', False)
                    week5 = dic.get('week5', False)
                    monday = dic.get('monday', False)
                    sunday = dic.get('sunday', False)
                    correct = False
                    if (january and december and week1 and week5 and monday and
                            sunday):
                        correct = True
                    self.assertEqual(
                        correct, True, 'Months, weeks and days erroneous')
