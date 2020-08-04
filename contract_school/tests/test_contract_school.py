# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo.tests import common
from .common import ContractSchoolCommon


@common.at_install(False)
@common.post_install(True)
class TestContractSchool(ContractSchoolCommon):

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
        self.assertEquals(invoice.child_id, self.contract.child_id)
        self.assertEquals(
            invoice.academic_year_id, self.contract.academic_year_id)
        self.assertEquals(invoice.school_id, self.contract.school_id)
        self.assertEquals(invoice.course_id, self.contract.course_id)
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
        invoice.action_invoice_open()
        self.assertEquals(invoice.state, "open")
        action_dict = invoice.create_account_payment_line()
        self.assertIn("domain", action_dict)
        self.assertEquals(
            "account.payment.order", action_dict.get("res_model"))

    def test_contract_school_wizard(self):
        self.assertTrue(self.journal.bank_account_id)
        self.assertEquals(
            self.journal.bank_account_id.partner_id, self.edu_partner)
        self.contract_model.cron_recurring_create_invoice()
        invoices = self.contract._get_related_invoices()
        self.assertEquals(len(invoices), 1)
        invoice = invoices[:1]
        invoice.action_invoice_open()
        payorder = self.payorder_model.create({
            "payment_mode_id": self.inbound_mode.id,
            "journal_id": self.journal.id,
        })
        field_list = self.payorder_wizard.fields_get_keys()
        wizard_vals = self.payorder_wizard.with_context(
            active_model=payorder._name,
            active_id=payorder.id).default_get(field_list)
        self.assertEquals(
            wizard_vals.get("bank_partner_id"),
            payorder.company_partner_bank_id.partner_id.id)
        wizard = self.payorder_wizard.new(wizard_vals)
        self.assertIn(
            ("school_id", "=", wizard_vals.get("bank_partner_id")),
            wizard._prepare_move_line_domain())
