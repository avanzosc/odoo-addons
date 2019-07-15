# -*- coding: utf-8 -*-
# (c) 2017 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import exceptions, fields, _
import openerp.tests.common as common
import base64
import os


class TestAccountMoveImport(common.TransactionCase):

    def setUp(self):
        super(TestAccountMoveImport, self).setUp()
        self.wiz_obj = self.env['import.account.move']
        self.agrolait = self.env.ref('base.res_partner_2')
        self.acc_move = self.env['account.move'].create(
            {'journal_id': self.env.ref('account.bank_journal').id,
             'period_id': self.env.ref('account.period_5').id,
             'date': fields.Date.today()
             })
        self.path = os.path.abspath(os.path.dirname(__file__))
        path1 = u'{}/move_data.csv'.format(self.path)
        file = open(path1, 'r')
        data = base64.encodestring(file.read())
        file.close()
        wiz_vals = {'data': data,
                    'name': 'move_data.csv',
                    'delimeter': ';'}
        self.wizard = self.wiz_obj.create(wiz_vals)

    def test_action_import_moves_csv(self):
        path2 = u'{}/error_file.xls'.format(self.path)
        with open(path2, 'r') as file:
            data = base64.encodestring(file.read())
        file.close()
        wiz_error_vals = {'data': data,
                          'name': 'error_file.xls',
                          'delimeter': ';'}
        wiz_error = self.wiz_obj.create(wiz_error_vals)
        wiz_error2_vals = {
            'data': base64.encodestring(u'no_name;key2\nTrue;data2'),
            'name': 'data_file.csv',
            'delimeter': ';'}
        wiz_error2 = self.wiz_obj.create(wiz_error2_vals)
        with self.assertRaises(exceptions.Warning):
            # No account move
            self.wizard.action_import_moves()
        with self.assertRaises(exceptions.Warning):
            # Invalid file
            wiz_error.with_context(
                active_id=self.acc_move.id).action_import_moves()
        with self.assertRaises(exceptions.Warning):
            # No key
            wiz_error2.with_context(
                active_id=self.acc_move.id).action_import_moves()
        self.wizard.with_context(
            active_id=self.acc_move.id).action_import_moves()
        self.assertEquals(self.acc_move.narration, u'No errors found',
                          'Error in import process')

    def test_exception_raise(self):
        wiz_error3_vals = {
            'data': base64.encodestring(
                u'account;name;debit;credit;parter_name;partner_type;date\n'
                u'X11006;X11006;;600;;;12-31-2016;'),
            'name': 'data_file.csv',
            'delimeter': ';'}
        self.wiz_obj.create(wiz_error3_vals)
#        wiz_error3 = self.wiz_obj.create(wiz_error3_vals)
#         with self.assertRaises(exceptions.Warning):
#             wiz_error3.with_context(
#                 active_id=self.acc_move.id).action_import_moves()

    def test_check_error_data(self):
        values = {'name': None}
        account_data = self.wizard._check_error_data(values)
        self.assertEquals(account_data['error'], _(u'Not line name defined'),
                          'No key "name" found')
        values = {'name': 'Agrolait'}
        account_data = self.wizard._check_error_data(values)
        self.assertEquals(account_data['error'], _(u'Account not found'),
                          'No account found')
        self.agrolait.ref = 'agrolait_ref'
        values.update({'partner_type': 'customer',
                       'partner_ref': 'agrolait_ref',
                       'credit': '-500'})
        account_data = self.wizard._check_error_data(values)
        self.assertEquals(account_data['error'], _(u"Wrong amount in account"),
                          'Invalid amount found')
        values.update({'debit': '400',
                       'credit': '0',
                       'currency': 'QWE',
                       'amount_currency': '200'})
        account_data = self.wizard._check_error_data(values)
        self.assertEquals(account_data['error'], _(u"Wrong currency code"),
                          'Invalid currency code')
        values.update({'debit': '400',
                       'credit': '0',
                       'currency': 'EUR',
                       'amount_currency': '200'})
        account_data = self.wizard._check_error_data(values)
        self.assertEquals(account_data['partner_id'], self.agrolait.id,
                          'Partner not found')
        values.pop('partner_ref')
        values.update({'partner_name': 'Agrolait'})
        account_data = self.wizard._check_error_data(values)
        self.assertEquals(account_data['partner_id'], self.agrolait.id,
                          'Partner not found')
        values.pop('partner_name')
        values.update({'partner_id': self.agrolait.id})
        account_data = self.wizard._check_error_data(values)
        self.assertEquals(account_data['partner_id'], self.agrolait.id,
                          'Partner not found')
