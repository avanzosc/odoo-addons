# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
import openerp.tests.common as common


class TestPurchaseLineWithDeliveryServiceInfo(common.TransactionCase):

    def setUp(self):
        super(TestPurchaseLineWithDeliveryServiceInfo, self).setUp()
        self.sale_model = self.env['sale.order']
        self.procurement_model = self.env['procurement.order']
        sale_vals = {
            'partner_id': self.env.ref('base.res_partner_1').id,
            'partner_shipping_id': self.env.ref('base.res_partner_1').id,
            'partner_invoice_id': self.env.ref('base.res_partner_1').id,
            'pricelist_id': self.env.ref('product.list0').id,
            'carrier_id': self.env.ref('delivery.normal_delivery_carrier').id}
        sale_line_vals = {
            'product_id': self.env.ref('product.product_product_6').id,
            'name': self.env.ref('product.product_product_6').name,
            'product_uos_qty': 1,
            'product_uom': self.env.ref('product.product_product_6').uom_id.id,
            'price_unit': self.env.ref('product.product_product_6').list_price}
        sale_vals['order_line'] = [(0, 0, sale_line_vals)]
        self.sale_order = self.sale_model.create(sale_vals)
        self.sale_order.delivery_set()
        for line in self.sale_order.order_line:
            if line.product_id.type == 'service':
                line.product_id.write(
                    {'route_ids':
                     [(6, 0,
                       [self.env.ref('stock.route_warehouse0_mto').id,
                        self.env.ref('purchase.route_warehouse0_buy').id])],
                     'seller_ids':
                     [(6, 0, [self.env.ref('base.res_partner_14').id])]})
                self.service_product = line.product_id
                line.write({'delivery_standard_price': 578.00})

    def test_confirm_sale_with_delivery_service(self):
        self.sale_order.action_button_confirm()
        cond = [('origin', '=', self.sale_order.name),
                ('product_id', '=', self.service_product.id)]
        procurement = self.procurement_model.search(cond)
        self.assertEqual(
            len(procurement), 1,
            "Procurement not generated for the service product type")
        procurement.run()
        cond = [('group_id', '=', procurement.group_id.id),
                ('product_id', '=', self.service_product.id),
                ('state', '=', 'confirmed')]
        procurement2 = self.procurement_model.search(cond)
        self.assertEqual(
            len(procurement2), 1,
            "Procurement2 not generated for the service product type")
        procurement2.run()
        self.assertTrue(
            bool(procurement2.purchase_id),
            "Purchase no generated for procurement Service")
        for line in procurement2.purchase_id.order_line:
            if line.product_id.type == 'service':
                self.assertEqual(
                    line.price_unit,
                    procurement2.sale_line_id.delivery_standard_price,
                    "Erroneous price on purchase order line")
