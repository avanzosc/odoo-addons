# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
import openerp.tests.common as common


class TestMrpProductionNoSplitFinishedProductMove(common.TransactionCase):

    def setUp(self):
        super(TestMrpProductionNoSplitFinishedProductMove, self).setUp()
        self.product_model = self.env['product.product']
        self.mrp_bom_model = self.env['mrp.bom']
        self.mrp_bom_line_model = self.env['mrp.bom.line']
        self.customer_model = self.env['res.partner']
        self.sale_model = self.env['sale.order']
        self.procurement_model = self.env['procurement.order']
        self.procurement_rule_model = self.env['procurement.rule']
        self.produce_model = self.env['mrp.product.produce']
        self.produce_line_model = self.env['mrp.product.produce.line']
        product_vals = {
            'name': 'Product to produce',
            'standard_price': 20.0,
            'list_price': 30.0,
            'type': 'product',
            'route_ids': [
                (6, 0,
                 [self.env.ref('mrp.route_warehouse0_manufacture').id,
                  self.env.ref('stock.route_warehouse0_mto').id])]}
        self.produce_product = self.product_model.create(product_vals)
        product_vals = {
            'name': 'Product to consume',
            'standard_price': 2.0,
            'list_price': 3.0,
            'type': 'product'}
        self.consume_product = self.product_model.create(product_vals)
        bom_vals = {'product_tmpl_id': self.produce_product.product_tmpl_id.id,
                    'product_id': self.produce_product.id}
        self.bom = self.mrp_bom_model.create(bom_vals)
        bom_line_vals = {'product_id': self.consume_product.id,
                         'bom_id': self.bom.id}
        self.mrp_bom_line_model.create(bom_line_vals)
        customer_vals = {'name': 'Customer-1',
                         'customer': True}
        self.customer = self.customer_model.create(customer_vals)
        sale_vals = {
            'partner_id': self.customer.id,
            'partner_shipping_id': self.customer.id,
            'partner_invoice_id': self.customer.id,
            'pricelist_id': self.env.ref('product.list0').id}
        sale_line_vals = {
            'product_id': self.produce_product.id,
            'name': self.produce_product.name,
            'product_uos_qty': 1,
            'product_uom': self.produce_product.uom_id.id,
            'price_unit': self.produce_product.list_price}
        sale_vals['order_line'] = [(0, 0, sale_line_vals)]
        self.sale_order = self.sale_model.create(sale_vals)

    def test_confirm_sale_for_produce_product(self):
        self.sale_order.action_button_confirm()
        cond = [('origin', '=', self.sale_order.name),
                ('product_id', '=', self.produce_product.id)]
        procurement = self.procurement_model.search(cond)
        self.assertEqual(
            len(procurement), 1,
            "Procurement not generated for produce product type")
        cond = [('group_id', '=', procurement.group_id.id),
                ('product_id', '=', self.produce_product.id),
                ('state', '=', 'confirmed')]
        procurement2 = self.procurement_model.search(cond)
        self.assertEqual(
            len(procurement2), 1,
            "Procurement2 not generated for produce product type")
        cond = [('name', 'ilike', 'Manufacture')]
        rule = self.procurement_rule_model.search(cond, limit=1)
        self.assertEqual(
            len(rule), 1, "Rule not found for MANUFACTURE")
        procurement2.write({'bom_id': self.bom.id,
                            'rule_id': rule.id})
        procurement2.run()
        self.assertTrue(
            bool(procurement2.production_id),
            "MRP production no generated for procurement2")
        procurement2.production_id.force_production()
        produce_vals = {'product_qty': 5,
                        'mode': 'consume_produce',
                        'product_id': self.produce_product.id,
                        'track_production': False}
        self.produce = self.produce_model.create(produce_vals)
        produce_line_vals = {'product_id': self.consume_product.id,
                             'product_qty': 1,
                             'produce_id': self.produce.id,
                             'track_production': False}
        self.produce_line_model.create(produce_line_vals)
        self.produce.with_context(
            active_id=procurement2.production_id.id).do_produce()
        self.assertEqual(
            len(procurement2.production_id.move_created_ids2), 1,
            "It has created more than one product to produce movement")
