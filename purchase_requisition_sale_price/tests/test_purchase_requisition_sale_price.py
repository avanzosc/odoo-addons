# -*- coding: utf-8 -*-
# (c) 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestPurchaseRequisitionSalePrice(common.TransactionCase):

    def setUp(self):
        super(TestPurchaseRequisitionSalePrice, self).setUp()
        self.sale_model = self.env['sale.order']
        self.product = self.browse_ref('product.product_product_5b')
        sale_vals = {
            'name': 'TestPurchaseRequisitionSalePrice',
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

    def test_purchase_requisition_sale_price(self):
        self.sale_order.button_create_purchase_requision_from_sale_order()
        self.assertNotEqual(len(self.sale_order.purchase_requisition_ids),
                            0, 'Purchase requisition no generated')
        line = self.sale_order.purchase_requisition_ids[0].line_ids[0]
        line.write({'transportation_price': 55.00,
                    'total_cost': 55.00,
                    'purchase_price': 80.00,
                    'margin': 0.014})
        line.onchange_margin()
        line._compute_psp_subtotal()
        self.assertEqual(
            line.psp_unit, line.sale_order_line_id.price_unit,
            'Sale order line price not equal purchase requisition price')
        self.sale_order.state = 'sent'
        requisition = self.sale_order.purchase_requisition_ids[0]
        requisition._compute_sale_amount_total()
        self.assertEqual(
            round(requisition.sale_amount_total, 2),
            round(self.sale_order.amount_total, 2),
            'Distinct amount of sale between sale order, and purchase'
            ' requisition')
        requisition._compute_purchase_amount_total()
        requisition._compute_margin()
        self.assertEqual(
            round(requisition.purchase_amount_total, 2),
            round(sum(requisition.line_ids.mapped('total_cost')), 2),
            'Distinct amount of purchase between purchase order, and purchase'
            ' requisition')
