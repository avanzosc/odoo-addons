# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common


class TestStockPickingServiceSale(common.TransactionCase):

    def setUp(self):
        super(TestStockPickingServiceSale, self).setUp()
        self.sale_model = self.env['sale.order']
        self.transfer_details_wizard = self.env['stock.transfer_details']
        self.picking_invoicing_wizard = self.env['stock.invoice.onshipping']
        self.picking_model = self.env['stock.picking']
        self.invoice_model = self.env['account.invoice']
        self.journal = self.env.ref('account.sales_journal')
        self.product = self.browse_ref(
            'product.product_product_7')
        self.service_product = self.browse_ref(
            'product.product_product_consultant')
        self.account_type = self.env['account.account.type'].create({
            'name': 'Test account type',
            'code': 'TEST',
        })
        self.account_tax = self.env['account.account'].create({
            'name': 'Test tax account',
            'code': 'TAX',
            'type': 'other',
            'user_type': self.account_type.id,
        })
        self.base_code = self.env['account.tax.code'].create({
            'name': '[28] Test base code',
            'code': 'TEST',
        })
        self.tax_code = self.env['account.tax.code'].create({
            'name': '[29] Test tax code',
            'code': 'TEST',
        })
        self.tax = self.env['account.tax'].create({
            'name': 'Test tax 10%',
            'type_tax_use': 'sale',
            'type': 'percent',
            'amount': '0.10',
            'account_collected_id': self.account_tax.id,
            'base_code_id': self.base_code.id,
            'base_sign': 1,
            'tax_code_id': self.tax_code.id,
            'tax_sign': 1,
        })
        self.base_code2 = self.env['account.tax.code'].create({
            'name': '[30] Test base code2',
            'code': 'TEST2',
        })
        self.tax_code2 = self.env['account.tax.code'].create({
            'name': '[31] Test tax code2',
            'code': 'TEST2',
        })
        self.tax2 = self.env['account.tax'].create({
            'name': 'Test tax 21%',
            'type_tax_use': 'sale',
            'type': 'percent',
            'amount': '0.21',
            'account_collected_id': self.account_tax.id,
            'base_code_id': self.base_code2.id,
            'base_sign': 1,
            'tax_code_id': self.tax_code2.id,
            'tax_sign': 1,
        })
        sale_vals = {
            'name': 'Test sale order',
            'partner_id': self.ref('base.res_partner_1'),
            'order_policy': 'picking'}
        sale_line_vals = {
            'product_id': self.service_product.id,
            'name': self.service_product.name,
            'product_uom_qty': 4,
            'tax_id': [(6, 0, self.tax.ids)],
            'product_uom': self.service_product.uom_id.id,
            'price_unit': 1000}
        sale_line_vals2 = {
            'product_id': self.product.id,
            'name': self.product.name,
            'product_uom_qty': 10,
            'tax_id': [(6, 0, self.tax.ids)],
            'product_uom': self.product.uom_id.id,
            'price_unit': 1000}
        sale_line_vals3 = {
            'product_id': self.service_product.id,
            'name': self.service_product.name,
            'product_uom_qty': 4,
            'tax_id': [(6, 0, self.tax2.ids)],
            'product_uom': self.service_product.uom_id.id,
            'price_unit': 1000}
        sale_line_vals4 = {
            'product_id': self.product.id,
            'name': self.product.name,
            'product_uom_qty': 10,
            'tax_id': [(6, 0, self.tax.ids)],
            'product_uom': self.product.uom_id.id,
            'price_unit': 1000}
        sale_vals['order_line'] = [(0, 0, sale_line_vals),
                                   (0, 0, sale_line_vals2),
                                   (0, 0, sale_line_vals3),
                                   (0, 0, sale_line_vals4)]
        self.sale_order = self.sale_model.create(sale_vals)
        self.sale_line_service = self.sale_order.order_line.filtered(
            lambda x: x.product_id == self.service_product)
        self.sale_line_no_service = self.sale_order.order_line.filtered(
            lambda x: x.product_id == self.product)
        try:
            self.sale_order.type_id.invoice_state = '2binvoiced'
        except Exception:
            pass
        self.sale_order.action_button_confirm()
        self.picking = self.sale_order.picking_ids[:1]
        self.picking.force_assign()

    def test_sale_to_picking(self):
        self.assertTrue(
            self.picking.sale_service_lines and
            self.picking.sale_service_lines.filtered(
                lambda x: x.sale_line_id in self.sale_line_service))
        self.picking.compute(self.picking)
        pick_tax = self.picking.taxes.filtered(lambda x: x.name ==
                                               'Test tax 10%')
        pick_tax2 = self.picking.taxes.filtered(lambda x: x.name ==
                                                'Test tax 21%')
        self.assertTrue(pick_tax)
        self.assertEqual(pick_tax.base, 24000)
        self.assertTrue(pick_tax2)
        self.assertEqual(pick_tax2.base, 4000)
        self.assertEqual(self.picking.amount_untaxed, 28000)
        self.assertEqual(self.picking.amount_tax,
                         (24000 * 0.10 + 4000 * 0.21))
        self.assertEqual(self.picking.amount_total,
                         (24000 * 0.10 + 4000 * 0.21) + 28000)
        self.picking.sale_service_lines.write({'in_picking': False})
        wizard = self.transfer_details_wizard.with_context(
            active_model='stock.picking', active_ids=[self.picking.id],
            active_id=self.picking.id).create({'picking_id': self.picking.id})
        for line in wizard.item_ids:
            line.quantity = 5
        wizard.do_detailed_transfer()
        self.assertEqual(self.picking.state, 'done')
        self.assertFalse(self.picking.sale_service_lines)
        backorder = self.picking_model.search(
            [('backorder_id', '=', self.picking.id)])
        self.assertTrue(
            backorder.sale_service_lines and
            backorder.sale_service_lines.filtered(
                lambda x: x.sale_line_id in self.sale_line_service))
        invoicing_wiz = self.picking_invoicing_wizard.with_context(
            active_model='stock.picking', active_ids=[self.picking.id],
            active_id=self.picking.id).create({'journal_id': self.journal.id,
                                               'journal_type': 'sale'})
        invoice_ids = invoicing_wiz.create_invoice()
        invoice = self.invoice_model.browse(invoice_ids[0])
        self.assertFalse(invoice.invoice_line.filtered(
            lambda x: x.product_id == self.service_product))
        invoicing_wiz = self.picking_invoicing_wizard.with_context(
            active_model='stock.picking', active_ids=[backorder.id],
            active_id=backorder.id).create({'journal_id': self.journal.id,
                                            'journal_type': 'sale'})
        invoice_ids = invoicing_wiz.create_invoice()
        invoice = self.invoice_model.browse(invoice_ids[0])
        self.assertTrue(invoice.invoice_line.filtered(
            lambda x: x.product_id == self.service_product))
