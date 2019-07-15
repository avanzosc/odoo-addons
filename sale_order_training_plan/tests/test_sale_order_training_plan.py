# -*- coding: utf-8 -*-
# (c) 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestSaleOrderTrainingPlan(common.TransactionCase):

    def setUp(self):
        super(TestSaleOrderTrainingPlan, self).setUp()
        self.training_plan_model = self.env['training.plan']
        self.sale_model = self.env['sale.order']
        training_plan_vals = {
            'name': 'Test sale order training plan 1',
            'resolution': 'Test sale order training plan resolution 1'}
        self.plan1 = self.training_plan_model.create(training_plan_vals)
        training_plan_vals = {
            'name': 'Test sale order training plan 2',
            'resolution': 'Test sale order training plan resolution 2'}
        self.plan2 = self.training_plan_model.create(training_plan_vals)
        self.product = self.browse_ref('product.product_product_35')
        self.product.product_training_ids = [
            (0, 0, {'product_tmpl_id': self.product.product_tmpl_id.id,
                    'product_id': self.product.id,
                    'sequence': 1,
                    'training_plan_id': self.plan1.id}),
            (0, 0, {'product_tmpl_id': self.product.product_tmpl_id.id,
                    'product_id': self.product.id,
                    'sequence': 2,
                    'training_plan_id': self.plan2.id})]
        sale_vals = {
            'name': 'sale order for training plan',
            'partner_id': self.ref('base.res_partner_18'),
            'pricelist_id': self.ref('product.list0')
        }
        sale_line_vals = {
            'product_id': self.product.id,
            'name': self.product.name,
            'product_uom_qty': 1,
            'product_uom': self.product.uom_id.id,
            'price_unit': self.product.list_price}
        sale_vals['order_line'] = [(0, 0, sale_line_vals)]
        self.sale_order = self.sale_model.create(sale_vals)

    def test_sale_order_training_plan(self):
        res = self.sale_order.order_line[0].product_id_change(
            self.ref('product.list0'), self.product.id,
            partner_id=self.ref('base.res_partner_18'))
        value = res.get('value', False)
        self.assertNotEqual(value, False,
                            'Not value found in product_id_change')
        training = value.get('training', False)
        self.assertNotEqual(training, False,
                            'Training not found in product_id_change')
        self.assertIn('1.- Test sale order training plan 1:', training,
                      'First training not found in sale order line')
        self.assertIn('2.- Test sale order training plan 2:', training,
                      'Second training not found in sale order line')
