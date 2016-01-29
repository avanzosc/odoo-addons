# -*- coding: utf-8 -*-
# (c) 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common
from openerp import exceptions


class TestAccountInvoiceTemporal(common.TransactionCase):

    def setUp(self):
        super(TestAccountInvoiceTemporal, self).setUp()
        self.invoice = self.env.ref('account.invoice_1')
        self.account = self.env.ref('account.a_sale')
        self.account.temporal = True

    def test_temporal(self):
        with self.assertRaises(exceptions.Warning):
            self.invoice.check_temporal()
        self.account.temporal = False
        self.invoice.check_temporal()
        self.assertNotEqual(self.invoice.state, 'draft')
