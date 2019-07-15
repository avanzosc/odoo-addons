# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common


class TestAccountInvoiceSupplierValidation(common.TransactionCase):

    def setUp(self):
        super(TestAccountInvoiceSupplierValidation, self).setUp()
        self.purchase_model = self.env['purchase.order']
        self.invoice_model = self.env['account.invoice']
        self.picking_model = self.env['stock.picking']
        self.employee = self.env.ref('hr.employee_qdp')
        self.admin_user = self.env['res.users'].search([('login', '=',
                                                         'admin')], limit=1)
        self.hr_department = self.env['hr.department'].create(
            {'name': 'Test Department', 'manager_id': self.employee.id})
        self.invoice = self.env.ref('account.invoice_2')
        self.invoice.type = 'out_invoice'
        self.invoice.name = 'Test supplier invoice validation'
        self.in_invoice = self.env.ref('account.demo_invoice_0')
        self.in_invoice.type = 'in_invoice'
        self.in_invoice.name = 'Test supplier invoice validation'
        self.partner = self.env.ref('base.res_partner_1')
        self.partner.hr_department = self.hr_department
        vals = self.purchase_model.onchange_partner_id(self.partner.id)
        value = vals.get('value')
        self.product = self.env.ref('product.product_product_4')
        purchase_line_vals = {
            'product_id': self.product.id,
            'name': self.product.name,
            'product_qty': 100,
            'price_unit': 5,
            'date_planned': '2016-02-25'}
        purchase_vals = {
            'partner_id': self.partner.id,
            'pricelist_id': value.get('pricelist_id'),
            'payment_term_id': value.get('payment_term_id'),
            'fiscal_position': value.get('fiscal_position'),
            'location_id': self.ref('stock.stock_location_locations_partner'),
            'state': 'draft',
            'invoice_method': 'order',
            'order_line': [(0, 0, purchase_line_vals)]}
        self.purchase = self.purchase_model.create(purchase_vals)

    def test_account_invoice_client_validation(self):
        out_refund = self.invoice.copy({'type': 'out_refund'})
        self.invoice.signal_workflow('invoice_open')
        self.assertEqual(self.invoice.state, 'open')
        out_refund.signal_workflow('invoice_open')
        self.assertEqual(out_refund.state, 'open')

    def test_account_invoice_supplier_validation(self):
        in_refund = self.in_invoice.copy({'type': 'in_refund'})
        self.in_invoice.signal_workflow('invoice_open')
        self.assertEqual(self.in_invoice.state, 'validation')
        in_refund.signal_workflow('invoice_open')
        self.assertEqual(in_refund.state, 'validation')
        self.in_invoice.signal_workflow('invoice_validation')
        self.assertEqual(self.in_invoice.state, 'open')
        in_refund.signal_workflow('invoice_validation')
        self.assertEqual(in_refund.state, 'open')

    def test_invoice_on_change(self):
        self.invoice.partner_id = self.partner
        self.invoice.user_id = self.admin_user
        res = self.invoice.onchange_partner_id(
            self.invoice.type, self.partner.id,
            date_invoice=self.invoice.date_invoice,
            company_id=self.invoice.company_id.id)
        self.assertFalse(res.get('value', {}).get('user_id', False))
        self.in_invoice.partner_id = self.partner
        self.in_invoice.user_id = self.admin_user
        res = self.in_invoice.onchange_partner_id(
            self.in_invoice.type, self.partner.id,
            date_invoice=self.in_invoice.date_invoice,
            company_id=self.in_invoice.company_id.id)
        self.assertNotEqual(res.get('value', {}).get('user_id', False),
                            self.admin_user.id)
        self.assertEqual(res.get('value', {}).get('user_id', False),
                         self.employee.user_id.id)

    def test_purchase_order_invoice(self):
        self.purchase.signal_workflow('purchase_confirm')
        invoice_id = self.purchase.view_invoice().get('res_id', False)
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(invoice.user_id, self.employee.user_id)

    def test_purchase_picking_invoice(self):
        self.purchase.invoice_method = 'picking'
        self.purchase.signal_workflow('purchase_confirm')
        picking_id = self.purchase.view_picking().get('res_id', False)
        picking = self.picking_model.browse(picking_id)
        invoice_ids = picking.action_invoice_create(
            journal_id=self.in_invoice.journal_id.id, group=True,
            type='in_invoice')
        for invoice in self.invoice_model.browse(invoice_ids):
            self.assertEqual(invoice.user_id, self.employee.user_id)
