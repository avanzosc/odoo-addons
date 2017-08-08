# -*- coding: utf-8 -*-
# Copyright 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common
from openerp import exceptions


class TestAccountInvoiceSupplierRefUniqueByFiscalYear(common.TransactionCase):

    def setUp(self):
        super(TestAccountInvoiceSupplierRefUniqueByFiscalYear, self).setUp()
        self.invoice_model = self.env['account.invoice']
        self.fiscalyear_model = self.env['account.fiscalyear']
        fiscalyear_vals = {'name': 'fiscal year 2020',
                           'code': '2020',
                           'date_start': '2020-01-01',
                           'date_stop': '2020-12-31',
                           'period_ids': [(0, 0, {'name': '2020-1',
                                                  'date_start': '2020-01-01',
                                                  'date_stop': '2020-06-30'}),
                                          (0, 0, {'name': '2020-2',
                                                  'date_start': '2020-07-01',
                                                  'date_stop': '2020-12-31'})]}
        self.fiscalyear2020 = self.fiscalyear_model.create(fiscalyear_vals)
        fiscalyear_vals = {'name': 'fiscal year 2021',
                           'code': '2021',
                           'date_start': '2021-01-01',
                           'date_stop': '2021-12-31',
                           'period_ids': [(0, 0, {'name': '2021-1',
                                                  'date_start': '2021-01-01',
                                                  'date_stop': '2021-06-30'}),
                                          (0, 0, {'name': '2021-2',
                                                  'date_start': '2021-07-01',
                                                  'date_stop': '2021-12-31'})]}
        self.fiscalyear2021 = self.fiscalyear_model.create(fiscalyear_vals)
        self.account = self.env['account.account'].search([], limit=1)

    def test_account_invoice_supplier_ref_unique_without_fiscalyear(self):
        invoice_vals = {'partner_id': self.ref('base.res_partner_13'),
                        'supplier_invoice_number': 'test_invoice_number 1',
                        'account_id': self.account.id,
                        'type': 'in_invoice'}
        self.invoice_model.create(invoice_vals)
        invoice_vals = {'partner_id': self.ref('base.res_partner_13'),
                        'supplier_invoice_number': 'test_invoice_number 1',
                        'account_id': self.account.id,
                        'type': 'in_invoice'}
        with self.assertRaises(exceptions.ValidationError):
            self.invoice_model.create(invoice_vals)

    def test_account_invoice_supplier_ref_unique_with_fiscalyear(self):
        invoice_vals = {'partner_id': self.ref('base.res_partner_13'),
                        'supplier_invoice_number': 'test_invoice_number 2',
                        'account_id': self.account.id,
                        'period_id': self.fiscalyear2020.period_ids[0].id,
                        'type': 'in_invoice'}
        self.invoice_model.create(invoice_vals)
        invoice_vals = {'partner_id': self.ref('base.res_partner_13'),
                        'supplier_invoice_number': 'test_invoice_number 2',
                        'account_id': self.account.id,
                        'period_id': self.fiscalyear2020.period_ids[0].id,
                        'type': 'in_invoice'}
        with self.assertRaises(exceptions.ValidationError):
            self.invoice_model.create(invoice_vals)
        invoice_vals = {'partner_id': self.ref('base.res_partner_13'),
                        'supplier_invoice_number': 'test_invoice_number 2',
                        'account_id': self.account.id,
                        'period_id': self.fiscalyear2020.period_ids[1].id,
                        'type': 'in_invoice'}
        with self.assertRaises(exceptions.ValidationError):
            self.invoice_model.create(invoice_vals)
        invoice_vals = {'partner_id': self.ref('base.res_partner_13'),
                        'supplier_invoice_number': 'test_invoice_number 2',
                        'account_id': self.account.id,
                        'period_id': self.fiscalyear2021.period_ids[0].id,
                        'type': 'in_invoice'}
        self.invoice_model.create(invoice_vals)
