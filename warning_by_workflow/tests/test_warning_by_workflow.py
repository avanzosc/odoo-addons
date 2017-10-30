# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common
from openerp import exceptions, fields


class TestWarningByWorkflow(common.TransactionCase):

    def setUp(self):
        super(TestWarningByWorkflow, self).setUp()
        self.wiz_model = self.env['partner.show.warning.wiz']
        self.purchase_model = self.env['purchase.order']
        self.product = self.browse_ref('product.product_product_7')
        partner_vals = {
            'name': 'Test Partner',
            'customer': True,
            'supplier': True,
            'picking_warn': 'no-message',
            'picking_warn_msg': 'Picking warning for partner',
            'sale_warn': 'no-message',
            'sale_warn_msg': 'Sale warning for partner',
            'purchase_warn': 'no-message',
            'purchase_warn_msg': 'Purchase warning for partner',
            'invoice_warn': 'no-message',
            'invoice_warn_msg': 'Invoice warning for partner',
            }
        self.partner = self.env['res.partner'].create(partner_vals)
        sale_line_vals = {
            'product_id': self.product.id,
            'name': self.product.name,
            'product_uom_qty': 10,
            'product_uom': self.product.uom_id.id,
            'price_unit': 1000
            }
        sale_vals = {
            'name': 'Test sale order',
            'partner_id': self.partner.id,
            'order_policy': 'picking',
            'order_line': [(0, 0, sale_line_vals)],
            }
        self.sale = self.env['sale.order'].create(sale_vals)
        vals = self.purchase_model.onchange_partner_id(self.partner.id)
        value = vals.get('value')
        purchase_line_vals = {
            'product_id': self.product.id,
            'name': self.product.name,
            'product_qty': 10,
            'product_uom': self.product.uom_id.id,
            'date_planned': fields.Date.today(),
            'price_unit': 1000
            }
        purchase_vals = {
            'name': 'Test purchase order',
            'partner_id': self.partner.id,
            'invoice_method': 'picking',
            'pricelist_id': value.get('pricelist_id'),
            'payment_term_id': value.get('payment_term_id'),
            'fiscal_position': value.get('fiscal_position'),
            'location_id': self.ref('stock.stock_location_locations_partner'),
            'order_line': [(0, 0, purchase_line_vals)],
            }
        self.purchase = self.purchase_model.create(purchase_vals)

    def test_no_message_warning(self):
        self.sale.action_button_confirm()
        self.assertEqual(self.sale.state, 'progress')
        self.purchase.purchase_confirm()
        self.assertEqual(self.purchase.state, 'approved')
        picking_id = self.purchase.view_picking().get('res_id')
        picking = self.env['stock.picking'].browse(picking_id)
        self.assertEqual(picking.invoice_state, '2binvoiced')
        res = picking.launch_create_invoice()
        self.assertEqual(res.get('res_model', False),
                         'stock.invoice.onshipping')

    def test_warning_sale_warning(self):
        self.product.type = 'product'
        self.sale.order_policy = 'picking'
        self.partner.picking_warn = 'warning'
        self.partner.invoice_warn = 'warning'
        res = self.sale.action_button_confirm()
        self.assertEqual(res.get('res_model'), 'partner.show.warning.wiz')
        message = self.wiz_model.browse(res.get('res_id')).exception_msg
        self.assertTrue(self.partner.picking_warn_msg in message)
        self.assertTrue(self.partner.invoice_warn_msg not in message)
        self.sale.order_policy = 'prepaid'
        res = self.sale.action_button_confirm()
        self.assertEqual(res.get('res_model'), 'partner.show.warning.wiz')
        message = self.wiz_model.browse(res.get('res_id')).exception_msg
        self.assertTrue(self.partner.picking_warn_msg not in message)
        self.assertTrue(self.partner.invoice_warn_msg in message)
        self.sale.order_policy = 'manual'
        res = self.sale.action_button_confirm()
        self.assertEqual(res.get('res_model'), 'partner.show.warning.wiz')
        message = self.wiz_model.browse(res.get('res_id')).exception_msg
        self.assertTrue(self.partner.picking_warn_msg in message)
        self.assertTrue(self.partner.invoice_warn_msg not in message)
        self.product.type = 'service'
        res = self.sale.action_button_confirm()
        self.assertEqual(self.sale.state, 'manual')
        res = self.sale.launch_create_invoice()
        self.assertEqual(res.get('res_model'), 'partner.show.warning.wiz')
        self.partner.invoice_warn = 'no-message'
        res = self.sale.launch_create_invoice()
        self.assertEqual(res.get('res_model'), 'sale.advance.payment.inv')

    def test_warning_purchase_picking_warning(self):
        self.product.type = 'product'
        self.partner.picking_warn = 'warning'
        self.partner.invoice_warn = 'warning'
        self.purchase.invoice_method = 'order'
        res = self.purchase.purchase_confirm()
        self.assertEqual(res.get('res_model'), 'partner.show.warning.wiz')
        message = self.wiz_model.browse(res.get('res_id')).exception_msg
        self.assertTrue(self.partner.picking_warn_msg in message)
        self.assertTrue(self.partner.invoice_warn_msg in message)
        self.purchase.invoice_method = 'picking'
        res = self.purchase.purchase_confirm()
        self.assertEqual(res.get('res_model'), 'partner.show.warning.wiz')
        message = self.wiz_model.browse(res.get('res_id')).exception_msg
        self.assertTrue(self.partner.picking_warn_msg in message)
        self.assertTrue(self.partner.invoice_warn_msg not in message)
        self.product.type = 'service'
        self.purchase.invoice_method = 'order'
        res = self.purchase.purchase_confirm()
        self.assertEqual(res.get('res_model'), 'partner.show.warning.wiz')
        message = self.wiz_model.browse(res.get('res_id')).exception_msg
        self.assertTrue(self.partner.picking_warn_msg not in message)
        self.assertTrue(self.partner.invoice_warn_msg in message)
        self.wiz_model.browse(res.get('res_id')).button_continue()
        self.assertEqual(self.purchase.state, 'approved')
        purchase2 = self.purchase.copy()
        self.product.type = 'product'
        self.partner.picking_warn = 'no-message'
        purchase2.invoice_method = 'picking'
        purchase2.purchase_confirm()
        self.assertEqual(purchase2.state, 'approved')
        picking_id = purchase2.view_picking().get('res_id')
        picking = self.env['stock.picking'].browse(picking_id)
        self.assertEqual(picking.invoice_state, '2binvoiced')
        res = picking.launch_create_invoice()
        self.assertEqual(res.get('res_model'), 'partner.show.warning.wiz')
        message = self.wiz_model.browse(res.get('res_id')).exception_msg
        self.assertTrue(self.partner.picking_warn_msg not in message)
        self.assertTrue(self.partner.invoice_warn_msg in message)

    def test_block_warning(self):
        self.product.type = 'product'
        self.partner.picking_warn = 'block'
        self.partner.invoice_warn = 'block'
        with self.assertRaises(exceptions.Warning):
            self.sale.action_button_confirm()
        self.purchase.invoice_method = 'order'
        with self.assertRaises(exceptions.Warning):
            self.purchase.purchase_confirm()
        self.partner.picking_warn = 'no-message'
        self.purchase.invoice_method = 'picking'
        self.purchase.purchase_confirm()
        picking_id = self.purchase.view_picking().get('res_id')
        picking = self.env['stock.picking'].browse(picking_id)
        self.assertEqual(picking.invoice_state, '2binvoiced')
        with self.assertRaises(exceptions.Warning):
            picking.launch_create_invoice()

    def test_mixed_wargning(self):
        self.partner.picking_warn = 'warning'
        self.partner.invoice_warn = 'block'
        self.purchase.invoice_method = 'order'
        with self.assertRaises(exceptions.Warning):
            self.purchase.purchase_confirm()
