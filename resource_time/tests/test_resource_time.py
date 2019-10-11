# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import odoo.tests.common as common


class TestResourceTime(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestResourceTime, cls).setUpClass()
        start_hour = 10.0
        cls.hour_gap = 4.0
        cls.calendar = cls.env['resource.calendar'].create({
            'name': 'Test Hour Gap',
            'attendance_ids': [
                (0, 0, {'dayofweek': '1',
                        'name': 'Day1',
                        'hour_from': start_hour,
                        'hour_to': start_hour + cls.hour_gap}),
                (0, 0, {'dayofweek': '2',
                        'name': 'Day2',
                        'hour_from': start_hour,
                        'hour_to': start_hour + cls.hour_gap})]
        })

    def test_resource_calendar(self):
        for attendance in self.calendar.attendance_ids:
            self.assertEquals(attendance.hour_gap, self.hour_gap)
        self.assertEquals(
            self.calendar.hour_gap,
            sum(self.calendar.mapped('attendance_ids.hour_gap')))
