# -*- coding: utf-8 -*-
# © 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.orgmichel fletcher/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestSaleUtilities(common.TransactionCase):

    def setUp(self):
        super(TestSaleUtilities, self).setUp()
        self.partner_model = self.env['res.partner']
        self.env.ref('base.res_partner_address_4').write(
            {'ref': 'REF15252683',
             'vat': 'ES15252683A'})
        self.sale = self.env.ref('sale.sale_order_1')
        self.sale.order_policy = 'manual'
        self.journal_id = self.env.ref('account.bank_journal')

    def test_sale_utilities(self):
        partners = self.partner_model.name_search('REF15252683')
        self.assertEqual(
            len(partners), 1, 'Partner not found by reference')
        partners = self.partner_model.name_search('ES15252683A')
        self.assertEqual(
            len(partners), 1, 'Partner not found by VAT')

    def test_sale_computed_fields(self):
        self.assertFalse(self.sale.shipped)
        self.assertFalse(self.sale.invoiced)
        self.sale.action_button_confirm()
        picks = self.sale.picking_ids
        picks.action_confirm()
        picks.force_assign()
        picks.action_done()
        self.assertTrue(self.sale.shipped)
        self.sale.action_invoice_create()
        invoices = self.sale.invoice_ids
        for inv in invoices:
            inv.signal_workflow('invoice_open')
            amount = inv.amount_total if inv.type == 'out_invoice' else \
                (inv.amount_total * -1)
            inv.pay_and_reconcile(
                pay_amount=amount,
                pay_account_id=self.journal_id.default_debit_account_id.id,
                period_id=inv.period_id.id, pay_journal_id=self.journal_id.id,
                writeoff_acc_id=self.journal_id.default_debit_account_id.id,
                writeoff_period_id=inv.period_id.id,
                writeoff_journal_id=self.journal_id.id, name='')
        self.assertTrue(self.sale.invoiced)
