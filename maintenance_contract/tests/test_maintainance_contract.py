# -*- coding: utf-8 -*-
# © 2017 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common


class TestMaintainanceContract(common.TransactionCase):

    def setUp(self):
        super(TestMaintainanceContract, self).setUp()
        self.contract = self.env.ref(
            'account.analytic_super_product_trainings')
        self.time_obj = self.env['hr.analytic.timesheet']
        self.product = self.ref('product.product_product_consultant')
        self.user = self.ref('base.partner_root')
        self.journal = self.ref('hr_timesheet.analytic_journal')
        self.hr_inv_obj = self.env['hr.timesheet.invoice.create']
        self.to_invoice = self.ref(
            'hr_timesheet_invoice.timesheet_invoice_factor1')
        self.account_obj = self.env['account.invoice']

    def test_maintainance_contract(self):
        self.contract.hours_per_month = 40.0
        time = self.time_obj.create({
            'name': 'Testing',
            'account_id': self.contract.id,
            'product_id': self.product,
            'unit_amount': 38.0,
            'user_id': self.user,
            'journal_id': self.journal,
            'to_invoice': self.to_invoice,
        })
        self.assertTrue(time)
        self.assertEqual(38.0, self.contract.consumed_hours)
        time1 = self.time_obj.create({
            'name': 'Testing 1',
            'account_id': self.contract.id,
            'product_id': self.product,
            'unit_amount': 4.0,
            'journal_id': self.journal,
            'to_invoice': self.to_invoice,
        })
        self.assertTrue(time1)
        self.assertEqual(-2, self.contract.remaining_hours_month)
        qty_invoice = sum(line.qty_invoice
                          for line in self.contract.line_ids.filtered(
                              lambda x: not x.invoice_id))
        self.assertEqual(2, qty_invoice)
        wiz = self.hr_inv_obj.with_context(
            active_ids=self.contract.line_ids.ids).create({})
        invoice = wiz.do_create()
        invoice_id = self.account_obj.browse(invoice['id'])
        self.assertTrue(invoice_id)
