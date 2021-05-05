# Copyright (c) 2021 Berezi Amubieta - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import common
from odoo import fields
import calendar


class TestEventRegistrationStudent(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestEventRegistrationStudent, cls).setUpClass()
        cond = [('state', '=', 'draft')]
        cls.registration = cls.env['event.registration'].search(cond, limit=1)
        cls.partner = cls.env['res.partner'].search([], limit=1)
        cond = [('id', '!=', cls.partner.id)]
        cls.student = cls.env['res.partner'].search(cond, limit=1)

    def test_event_registration_student(self):
        self.registration.event_id.customer_id = self.partner
        self.registration._onchange_student_id()
        self.assertEqual(self.registration.name, self.partner.name)
        self.assertEqual(self.registration.email, self.partner.email)
        self.assertEqual(self.registration.phone, self.partner.phone)
        self.assertEqual(self.registration.mobile, self.partner.mobile)
        self.registration.student_id = self.student.id
        self.registration._onchange_student_id()
        self.assertEqual(self.registration.name, self.student.name)
        self.assertEqual(self.registration.email, self.student.email)
        self.assertEqual(self.registration.phone, self.student.phone)
        self.assertEqual(self.registration.mobile, self.student.mobile)
        self.registration.action_confirm()
        self.assertEqual(self.registration.real_date_start,
                         fields.Date.today())
        self.assertEqual(self.registration.date_start.day, 1)
        last_month_day = calendar.monthrange(
            fields.Date.today().year,
            fields.Date.today().month)[1]
        date_end = fields.Date.today().replace(day=last_month_day)
        self.registration.action_cancel()
        self.assertEqual(self.registration.real_date_end,
                         fields.Date.today())
        self.assertEqual(self.registration.date_end, date_end)
        self.registration.action_set_done()
        self.assertEqual(self.registration.real_date_end,
                         fields.Date.today())
        self.assertEqual(self.registration.date_end, date_end)
        self.registration.action_set_draft()
        self.assertEqual(self.registration.real_date_start, False)
        self.assertEqual(self.registration.date_start, False)
        self.assertEqual(self.registration.real_date_end, False)
        self.assertEqual(self.registration.date_end, False)
