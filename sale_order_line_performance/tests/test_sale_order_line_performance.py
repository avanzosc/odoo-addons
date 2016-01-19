# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestSaleOrderLinePerformance(common.TransactionCase):

    def setUp(self):
        super(TestSaleOrderLinePerformance, self).setUp()
        self.sale_model = self.env['sale.order']
        self.product = self.env.ref('product.product_product_consultant')
        self.product.performance = 5.0
        sale_vals = {
            'partner_id': self.ref('base.res_partner_1'),
            'partner_shipping_id': self.ref('base.res_partner_1'),
            'partner_invoice_id': self.ref('base.res_partner_1'),
            'pricelist_id': self.env.ref('product.list0').id}
        sale_line_vals = {
            'product_id': self.product.id,
            'name': self.product.name,
            'product_uos_qty': 7,
            'product_uom': self.product.uom_id.id,
            'price_unit': self.product.list_price}
        sale_vals['order_line'] = [(0, 0, sale_line_vals)]
        self.sale_order = self.sale_model.create(sale_vals)

    def test_sale_order_line_performance(self):
        line = self.sale_order.order_line[0]
        res = line.product_id_change(
            self.sale_order.pricelist_id.id, line.product_id.id,
            qty=line.product_uom_qty, qty_uos=line. product_uos_qty,
            name=line.name, partner_id=self.sale_order.partner_id.id,
            update_tax=True, date_order=self.sale_order.date_order,
            fiscal_position=self.sale_order.fiscal_position.id)
        self.assertEqual(
            self.product.performance, res['value'].get('performance', 0),
            'Different performances')
        self.assertEqual(
            line.price_subtotal,
            line.price_unit * line.performance * line.product_uom_qty,
            'Error in sale orde line subtotal')
