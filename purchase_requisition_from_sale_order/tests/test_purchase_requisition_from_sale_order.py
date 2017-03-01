# -*- coding: utf-8 -*-
# (c) 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestPurchaseRequisitionFromSaleOrder(common.TransactionCase):

    def setUp(self):
        super(TestPurchaseRequisitionFromSaleOrder, self).setUp()
        self.sale_model = self.env['sale.order']
        self.product = self.browse_ref('product.product_product_5b')
        sale_vals = {
            'name': 'TestPurchaseRequisitionFromSaleOrder',
            'partner_id': self.ref('base.res_partner_1'),
        }
        sale_line_vals = {
            'product_id': self.product.id,
            'name': self.product.name,
            'product_uom_qty': 7,
            'product_uom': self.product.uom_id.id,
            'price_unit': self.product.list_price}
        sale_vals['order_line'] = [(0, 0, sale_line_vals)]
        self.sale_order = self.sale_model.create(sale_vals)

    def test_purchase_requisition_from_sale_order(self):
        self.sale_order.button_create_purchase_requision_from_sale_order()
        self.sale_order._compute_count_requisitions()
        self.assertEqual(
            self.sale_order.count_requisitions, 1,
            'Purchase requisition not generated')
        self.assertNotEqual(len(self.sale_order.purchase_requisition_ids),
                            0, 'Purchase requisition no generated')
        requisition = self.sale_order.purchase_requisition_ids[0]
        self.assertEqual(
            requisition.line_ids[0].product_id,
            self.sale_order.order_line[0].product_id,
            'Product not found in purchase requisition')
        self.assertEqual(
            requisition.line_ids[0].sale_order_line_id.id,
            self.sale_order.order_line[0].id,
            'Purchase requisition line without sale order line info')
        result = self.sale_order.show_calls_for_bids()
        domain = result.get('domain')
        self.assertEqual(
            domain[0][2],
            self.sale_order.mapped('purchase_requisition_ids').ids)
