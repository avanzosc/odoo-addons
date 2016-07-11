# -*- coding: utf-8 -*-
# (c) 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestPartnerContactBirthdateAge(common.TransactionCase):

    def setUp(self):
        super(TestPartnerContactBirthdateAge, self).setUp()
        self.partner = self.env.ref('base.res_partner_26')

    def test_partner_contact_birthdate_age(self):
        self.partner.birthdate_date = '1969-12-19'
        self.partner._compute_partner_years()
        self.assertNotEqual(
            self.partner.age, 0, 'Partner without age')
