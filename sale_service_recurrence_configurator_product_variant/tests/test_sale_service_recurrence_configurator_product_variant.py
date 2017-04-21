# -*- coding: utf-8 -*-
# (c) 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestSaleServiceRecurrenceConfiguratorProductVariant(
        common.TransactionCase):

    def setUp(self):
        super(TestSaleServiceRecurrenceConfiguratorProductVariant,
              self).setUp()
        self.sale_model = self.env['sale.order']
        self.line_template = self.env.ref(
            'website_quote.website_sale_order_line_1')
        self.line_template.write(
            {'january': True,
             'december': True,
             'week1': True,
             'week5': True,
             'monday': True,
             'sunday': True,
             'product_template':
             self.line_template.product_id.product_tmpl_id.id})
        sale_vals = {
            'partner_id': self.ref('base.res_partner_1'),
            'partner_shipping_id': self.ref('base.res_partner_1'),
            'partner_invoice_id': self.ref('base.res_partner_1'),
            'pricelist_id': self.env.ref('product.list0').id,
            'template_id': self.line_template.quote_id.id}
        self.sale_order = self.sale_model.create(sale_vals)

    def test_sale_service_recurrence_configurator_pvariant(self):
        res = self.sale_order.onchange_template_id(
            self.line_template.quote_id.id,
            partner=self.ref('base.res_partner_1'))
        product_tmpl_id = self.line_template.product_id.product_tmpl_id.id
        cond = "'product_tmpl_id': " + str(product_tmpl_id)
        self.assertNotIn(cond, res.get('value'),
                         'Bad product_tmpl_id')
