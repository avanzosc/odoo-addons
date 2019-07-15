# -*- coding: utf-8 -*-
# © 2016 Alfredo de la Fuente - AvanzOSC
# © 2016 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestPurchaseLineWithDeliveryServiceInfo(common.TransactionCase):

    def setUp(self):
        super(TestPurchaseLineWithDeliveryServiceInfo, self).setUp()
        self.sale_model = self.env['sale.order']
        self.procurement_model = self.env['procurement.order']
        product_model = self.env['product.product']
        partner_model = self.env['res.partner']
        carrier_partner = partner_model.create({
            'name': 'Partner for carrier tests',
            'customer': False,
            'supplier': False,
        })
        customer_partner = partner_model.create({
            'name': 'Customer for test',
            'customer': True,
            'supplier': False,
        })
        supplier_partner = partner_model.create({
            'name': 'Supplier for test',
            'customer': False,
            'supplier': True,
        })
        sale_product = product_model.create({
            'name': 'Product for test',
            'type': 'consu',
            'list_price': 100.0,
            'uom_id': self.ref('product.product_uom_unit'),
        })
        self.carrier_product = product_model.create({
            'name': 'Carrier product for test',
            'type': 'service',
            'list_price': 10.0,
            'route_ids': [(6, 0,
                           [self.env.ref('stock.route_warehouse0_mto').id,
                            self.env.ref('purchase.route_warehouse0_buy').id
                            ])]})
        self.env['product.supplierinfo'].create({
            'name': supplier_partner.id,
            'product_tmpl_id': self.carrier_product.product_tmpl_id.id,
        })
        carrier = self.env['delivery.carrier'].create({
            'name': 'Carrier for test',
            'partner_id': carrier_partner.id,
            'product_id': self.carrier_product.id,
            'normal_price': 20.0,
        })
        sale_vals = {
            'partner_id': customer_partner.id,
            'carrier_id': carrier.id,
        }
        sale_line_vals = {
            'product_id': sale_product.id,
            'name': sale_product.name,
            'product_uos_qty': 1.0,
            'product_uom': sale_product.uom_id.id,
            'price_unit': sale_product.list_price}
        sale_vals['order_line'] = [(0, 0, sale_line_vals)]
        self.sale_order = self.sale_model.create(sale_vals)
        self.sale_order.delivery_set()

    def test_confirm_sale_with_delivery_service(self):
        self.sale_order.action_button_confirm()
        procurement = self.procurement_model.search(
            [('product_id', '=', self.carrier_product.id)], limit=1)
        self.assertEqual(
            len(procurement), 1,
            "Sale procurement not generated for carrier service product.")
        procurement.run()
        self.assertTrue(procurement.state == 'running')
        self.assertTrue(
            bool(procurement.purchase_id),
            "Purchase order not generated for procurement carrier service.")
        self.assertEqual(
            procurement.purchase_line_id.price_unit,
            procurement.sale_line_id.delivery_standard_price,
            "Erroneous price on purchase order line")
