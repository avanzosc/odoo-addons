# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo.tests import common
from odoo import fields
from dateutil.relativedelta import relativedelta


@common.at_install(False)
@common.post_install(True)
class TestContractSchool(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestContractSchool, cls).setUpClass()
        cls.product_model = cls.env['product.product']
        cls.contract_model = cls.env['contract.contract']
        cls.line_model = cls.env['contract.line']
        cls.partner_model = cls.env['res.partner']
        cls.invoice_model = cls.env['account.invoice']
        cls.tax_model = cls.env['account.tax']
        today = fields.Date.from_string(fields.Date.today())
        start = today + relativedelta(months=-1)
        end = today + relativedelta(months=+1)
        family_vals = {
            'name': 'Family for test sale_crm_school',
            'educational_category': 'family',
        }
        cls.tax_10 = cls.tax_model.create({
            'name': '10% Tax',
            'amount_type': 'percent',
            'amount': 10,
        })
        cls.tax_20 = cls.tax_model.create({
            'name': '20% Tax',
            'amount_type': 'percent',
            'amount': 20,
        })
        cls.family = cls.partner_model.create(family_vals)
        cls.product1 = cls.product_model.create({
            'name': 'Test Service 10%',
            'type': 'service',
            'taxes_id': [(6, 0, cls.tax_10.ids)],
        })
        cls.product2 = cls.product_model.create({
            'name': 'Test Product 20%',
            'type': 'product',
            'taxes_id': [(6, 0, cls.tax_20.ids)],
        })
        contract_vals = {
            'name': 'Contract for test contract_school',
            'partner_id': cls.family.id,
            'contract_type': 'sale',
        }
        cls.contract = cls.contract_model.create(contract_vals)
        line_vals = {
            'contract_id': cls.contract.id,
            'product_id': cls.product1.id,
            'name': cls.product1.name,
            'uom_id': cls.product1.uom_id.id,
            'recurring_next_date': today,
            'date_start': start,
            'date_end': end,
        }
        cls.line = cls.line_model.create(line_vals)
        cls.line._onchange_product_id()
        cls.line.write({
            'price_unit': 800,
            'payment_percentage': 50.0,
        })
        cls.line2 = cls.line.copy()
        cls.line2._onchange_product_id()
        cls.line2.write({
            'product_id': cls.product2.id,
            'name': cls.product2.name,
            'price_unit': 200,
            'payment_percentage': 100.0,
            'recurring_next_date': start,
            'date_end': start,
        })
        cls.line3 = cls.line.copy()
        cls.line3._onchange_product_id()
        cls.line3.write({
            'price_unit': 300,
            'payment_percentage': 100.0,
            'recurring_next_date': end,
        })

    def test_contract_school(self):
        for line in self.contract.contract_line_ids:
            subtotal = line.quantity * line.price_unit
            subtotal *= (1 - (line.discount / 100))
            subtotal *= line.payment_percentage / 100
            self.assertEquals(line.price_subtotal, subtotal)
        self.contract_model.cron_recurring_create_invoice()
        invoices = self.contract._get_related_invoices()
        self.assertEquals(len(invoices), 1)
        invoice = invoices[:1]
        self.assertEquals(invoice.amount_untaxed, 600)
        self.assertEquals(invoice.amount_tax, 80)
        self.assertEquals(invoice.amount_total, 680)
        self.assertEquals(len(invoice.invoice_line_ids), 2)
        invoice_line = invoice.invoice_line_ids[:1]
        self.assertEquals(invoice_line.payment_percentage, 50.0)
        self.assertEquals(invoice_line.price_subtotal_signed, 400.0)
        self.assertEquals(invoice_line.price_subtotal, 400.0)
        self.assertEquals(invoice_line.price_total, 440.0)
        self.assertEquals(invoice_line.price_tax, 40.0)
        self.assertEquals(len(invoice.tax_line_ids), 2)
        tax_line = invoice.tax_line_ids.filtered(
            lambda l: l.tax_id in invoice_line.invoice_line_tax_ids)
        self.assertEquals(tax_line.amount, invoice_line.price_tax)
        self.assertEquals(tax_line.base, invoice_line.price_subtotal)
        self.assertEquals(
            invoice.amount_untaxed,
            sum(invoice.mapped('invoice_line_ids.price_subtotal')))
        self.assertEquals(
            invoice.amount_untaxed,
            sum(invoice.mapped('tax_line_ids.base')))
        self.assertEquals(
            invoice.amount_tax,
            sum(invoice.mapped('invoice_line_ids.price_tax')))
        self.assertEquals(
            invoice.amount_tax,
            sum(invoice.mapped('tax_line_ids.amount')))
        self.assertEquals(
            invoice.amount_total,
            sum(invoice.mapped('invoice_line_ids.price_total')))
