# -*- coding: utf-8 -*-
# © 2016 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common


class TestHrCalendarZone(common.TransactionCase):

    def setUp(self):
        super(TestHrCalendarZone, self).setUp()
        self.employee = self.env.ref('hr.employee')
        self.partner = self.env.ref('base.partner_root')
        self.partner.zone_ids = [(6, 0, [
            self.ref('partner_zone.zone1'),
            self.ref('partner_zone.zone2'),
        ])]
        self.employee.address_home_id = self.partner
        self.attendance = self.env.ref('resource.calendar_attendance_mon1')

    def test_onchange_emp_id(self):
        self.attendance.emp_id = self.employee.id
        res = self.attendance.onchange_emp_id()
        attendance_res = self.env['res.partner.zone'].search(
            res['domain']['zone_id'])
        self.assertEqual(len(attendance_res), 2)
