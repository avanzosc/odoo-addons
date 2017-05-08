# -*- coding: utf-8 -*-
# (c) 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestSaleOrderLineServiceView(common.TransactionCase):

    def setUp(self):
        super(TestSaleOrderLineServiceView, self).setUp()
        self.sale_model = self.env['sale.order']
        self.wiz_model = self.env['wiz.delete.sale.line']
        service_product = self.env.ref('product.product_product_consultant')
        sale_vals = {
            'name': 'sale order 1',
            'partner_id': self.ref('base.res_partner_1'),
            'partner_shipping_id': self.ref('base.res_partner_1'),
            'partner_invoice_id': self.ref('base.res_partner_1'),
            'pricelist_id': self.env.ref('product.list0').id,
        }
        sale_line_vals = {
            'product_id': service_product.id,
            'name': service_product.name,
            'product_uom_qty': 7,
            'product_uos_qty': 7,
            'product_uom': service_product.uom_id.id,
            'price_unit': service_product.list_price}
        sale_vals['order_line'] = [(0, 0, sale_line_vals)]
        self.sale_order = self.sale_model.create(sale_vals)

    def test_sale_order_line_service_view(self):
        wiz = self.wiz_model.with_context(
            active_ids=self.sale_order.ids).create({})
        wiz.lines.write({'delete_record': True})
        wiz.button_delete_sale_lines()
        self.assertEqual(
            len(self.sale_order.order_line), 0, 'Sale order with line')

    def test_sale_order_line_service(self):
        self.assertEquals(len(self.sale_order.order_line), 1)
        for line in self.sale_order.order_line:
            line.invalidate_cache()
        self.assertEquals(self.sale_order.order_line,
                          self.sale_order.service_order_line |
                          self.sale_order.no_service_order_line)
        self.assertEquals(len(self.sale_order.service_order_line), 1)
