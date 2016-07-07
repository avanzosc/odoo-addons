# -*- coding: utf-8 -*-
# (c) 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestPartnerContactBirthdateYear(common.TransactionCase):

    def setUp(self):
        super(TestPartnerContactBirthdateYear, self).setUp()
        self.partner = self.ref('base.public_partner')

    def test_partner_contact_birthdate_year(self):
        self.partner.birthdate_date = '1969-12-19'
        self.assertNotEqual(
            self.partner.age, 0, 'Partner without age')
