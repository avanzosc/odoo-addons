# Copyright 2021 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from .common import TestContactBirthdateCommon
from odoo.tests import common
from dateutil.relativedelta import relativedelta


@common.at_install(False)
@common.post_install(True)
class TestContactBirthdate(TestContactBirthdateCommon):

    def test_today_birthdate(self):
        bday_partners = self.partner_obj.search([
            ("birthday_today", "=", self.today),
        ])
        self.assertTrue(self.bday_today.birthday_today)
        self.assertIn(self.bday_today, bday_partners)

    def test_next_week_birthdays(self):
        partners = self.partner_obj.next_week_birthday()
        birthday_dates = partners.mapped("birthdate_date")
        self.assertTrue(len(partners) >= 7)
        min_date = min(birthday_dates)
        self.assertEquals(min_date, self.today + relativedelta(days=1))
        max_date = max(birthday_dates)
        self.assertEquals(max_date, self.today + relativedelta(days=7))
