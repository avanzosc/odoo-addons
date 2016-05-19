# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestWebsiteQuoteNotUnlink(common.TransactionCase):

    def setUp(self):
        super(TestWebsiteQuoteNotUnlink, self).setUp()
        self.sale_model = self.env['sale.order']
        service_product = self.env.ref('product.product_product_consultant')
        sale_vals = {
            'name': 'sale order 1',
            'partner_id': self.ref('base.res_partner_1'),
            'partner_shipping_id': self.ref('base.res_partner_1'),
            'partner_invoice_id': self.ref('base.res_partner_1'),
            'pricelist_id': self.env.ref('product.list0').id}
        sale_line_vals = {
            'product_id': service_product.id,
            'name': service_product.name,
            'product_uom_qty': 7,
            'product_uos_qty': 7,
            'product_uom': service_product.uom_id.id,
            'price_unit': 25}
        sale_vals['order_line'] = [(0, 0, sale_line_vals)]
        self.sale_order = self.sale_model.create(sale_vals)

    def test_website_quote_not_unlink(self):
        res = self.sale_order.onchange_template_id(
            1, order_line=[(6, 0, [self.sale_order.order_line[0].id])],
            partner=self.ref('base.res_partner_1'))
        self.assertNotEqual(
            len(res), 0, 'Change without data')
        res = self.sale_order.onchange_template_id(
            1,
            order_line=[
                (0, 0, {'product_uos_qty': 1.0, 'product_id': 57,
                        'product_uom': 1, 'price_unit': 12950.0,
                        'product_uom_qty': 1.0, 'discount': 10.0,
                        'state': 'draft', 'th_weight': 0.0,
                        'product_uos': False,
                        'tax_id': [(6, 0, [])],
                        'name': 'Formacion funcional'})],
            partner=self.ref('base.res_partner_1'))
        self.assertNotEqual(
            len(res), 0, 'Change without data 2')
