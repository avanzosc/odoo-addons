# -*- coding: utf-8 -*-
# (c) 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestPurchaseRequisitionPurchasePrice(common.TransactionCase):

    def setUp(self):
        super(TestPurchaseRequisitionPurchasePrice, self).setUp()
        self.requisition_model = self.env['purchase.requisition']
        self.wiz_model = self.env['purchase.requisition.partner']
        self.product = self.browse_ref('product.product_product_5b')
        requisition_vals = {'exclusive': 'multiple'}
        requision_line_vals = {
            'product_id': self.product.id,
            'product_qty': 20}
        requisition_vals['line_ids'] = [(0, 0, requision_line_vals)]
        self.requisition = self.requisition_model.create(requisition_vals)

    def test_purchase_requisition_purchase_price(self):
        wiz_vals = {'partner_id': self.browse_ref('base.res_partner_13').id}
        wiz = self.wiz_model.create(wiz_vals)
        wiz.with_context(active_ids=self.requisition.ids).create_order()
        wiz_vals = {'partner_id': self.browse_ref('base.res_partner_1').id}
        wiz = self.wiz_model.create(wiz_vals)
        wiz.with_context(active_ids=self.requisition.ids).create_order()
        line = self.requisition.line_ids[0]
        line.onchange_purchase_price_transportation_price()
        line.purchase_line_ids[0].write({
            'product_qty': 5,
            'price_unit': 6.00})
        self.requisition.line_ids[0].purchase_line_ids[1].write({
            'product_qty': 40,
            'price_unit': 20.00})
        self.assertEqual(
            self.requisition.line_ids[0].purchase_price,
            330, 'Error in purchase price of purchase requisition product')
        self.assertEqual(
            self.requisition.line_ids[0].unit_cost, 16.5,
            'Error in unit cost')
        self.requisition.line_ids[0].purchase_line_ids[1].unlink()
        self.assertEqual(
            self.requisition.line_ids[0].purchase_price,
            30, 'Error2 in purchase price of purchase requisition product')
