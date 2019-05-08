# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo.tests.common import TransactionCase
from odoo import fields
from dateutil.relativedelta import relativedelta


class TestContractSchool(TransactionCase):

    def setUp(self):
        super(TestContractSchool, self).setUp()
        self.product_model = self.env['product.product']
        self.account_model = self.env['account.analytic.account']
        self.line_model = self.env['account.analytic.invoice.line']
        self.partner_model = self.env['res.partner']
        self.invoice_model = self.env['account.invoice']
        today = fields.Date.from_string(fields.Date.today())
        yesterday = today + relativedelta(days=-1)
        tomorrow = today + relativedelta(days=+1)
        family_vals = {
            'name': 'Family for test sale_crm_school',
            'educational_category': 'family'}
        self.family = self.partner_model.create(family_vals)
        self.product = self.product_model.search([], limit=1)
        account_vals = {
            'name': 'Contract for test contract_school',
            'partner_id': self.family.id,
            'contract_type': 'sale',
            'recurring_invoices': True}
        self.account = self.account_model.create(account_vals)
        self.account.date_start = today + relativedelta(months=-2)
        line_vals = {
            'analytic_account_id': self.account.id,
            'product_id': self.product.id,
            'name': self.product.name,
            'uom_id': self.product.uom_id.id}
        self.line = self.line_model.create(line_vals)
        self.line._onchange_product_id()
        self.line.write({
            'price_unit': 800,
            'payment_percentage': 50.0})
        line_vals = {
            'analytic_account_id': self.account.id,
            'product_id': self.product.id,
            'name': self.product.name,
            'uom_id': self.product.uom_id.id}
        self.line = self.line_model.create(line_vals)
        self.line._onchange_product_id()
        self.line.write({
            'price_unit': 200,
            'payment_percentage': 100.0,
            'from_date': tomorrow})
        line_vals = {
            'analytic_account_id': self.account.id,
            'product_id': self.product.id,
            'name': self.product.name,
            'uom_id': self.product.uom_id.id,
            'price_unit': 300,
            'payment_percentage': 100.0}
        self.line = self.line_model.create(line_vals)
        self.line._onchange_product_id()
        self.line.write({
            'price_unit': 300,
            'payment_percentage': 100.0,
            'to_date': yesterday})

    def test_contract_school(self):
        for line in self.account.recurring_invoice_line_ids:
            line._compute_price_subtotal()
        self.account_model.cron_recurring_create_invoice()
        cond = [('partner_id', '=', self.family.id)]
        invoice = self.invoice_model.search(cond, limit=1)
        self.assertEquals(len(invoice.invoice_line_ids), 1)
        self.assertEquals(invoice.invoice_line_ids[0].payment_percentage, 50.0)
        self.assertEquals(invoice.invoice_line_ids[0].price_subtotal, 400.0)
