# -*- coding: utf-8 -*-
# © 2016 Ainara Galdona - AvanzOSC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import openerp.tests.common as common
from openerp import _


class TestCrmLeadPartnerContact(common.TransactionCase):

    def setUp(self):
        super(TestCrmLeadPartnerContact, self).setUp()
        self.partner_model = self.env['res.partner']
        self.partner = self.partner_model.create(
            {'name': 'Test',
             'email': 'test@test.com',
             'phone': '999 012 345',
             'mobile': '666 012 345',
             'fax': '999 012 344',
             })

    def test_name_get_email(self):
        res = self.partner.with_context(show_also_email=True).name_get()
        for record in res:
            partner = self.partner_model.browse(record[0])
            if partner.email:
                self.assertTrue(_('Email:') in record[1])
            else:
                self.assertFalse(_('Email:') in record[1])
        res = self.partner.with_context(show_email=False).name_get()
        for record in res:
            self.assertFalse(_('Email:') in record[1])

    def test_name_get_phone(self):
        res = self.partner.with_context(show_phones=True).name_get()
        for record in res:
            partner = self.partner_model.browse(record[0])
            if partner.phone:
                self.assertTrue(_('Phone:') in record[1])
            else:
                self.assertFalse(_('Phone:') in record[1])
            if partner.mobile:
                self.assertTrue(_('Mobile:') in record[1])
            else:
                self.assertFalse(_('Mobile:') in record[1])
            if partner.fax:
                self.assertTrue(_('Fax:') in record[1])
            else:
                self.assertFalse(_('Fax:') in record[1])
        res = self.partner.with_context(show_phones=False).name_get()
        for record in res:
            self.assertFalse(_('Phone:') in record[1])
            self.assertFalse(_('Mobile:') in record[1])
            self.assertFalse(_('Fax:') in record[1])
