# Copyright (c) 2021 Berezi Amubieta - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import common, tagged
from odoo import fields


@tagged("post_install", "-at_install")
class TestEventTrackReplanification(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestEventTrackReplanification, cls).setUpClass()
        cls.calendar35 = cls.env.ref('resource.resource_calendar_std_35h')
        cls.calendar40 = cls.env.ref('resource.resource_calendar_std')
        days = cls.calendar35.attendance_ids.filtered(
            lambda x: x.dayofweek != '0')
        days.unlink()
        date_start = fields.Datetime.from_string('2021-11-01 08:00:00')
        date_end = fields.Datetime.from_string('2021-11-30 10:00:00')
        event_vals = {
            'name': 'Event for event track replanification',
            'date_begin': date_start,
            'date_end': date_end,
            'resource_calendar_id': cls.calendar35.id
            }
        cls.event = cls.env['event.event'].create(event_vals)
        cls.stage = cls.env.ref('event.event_stage_announced')

    def test_event_create_track(self):
        self.event.stage_id = self.stage.id
        self.assertEqual(len(self.event.track_ids), 10)
        self.event.write({
            'replan_date_begin': '2021-11-01',
            'replan_date_end': '2021-11-30',
            'replan_resource_calendar_id': self.calendar40.id})
        self.event.button_replan_sessions()
        self.assertEqual(len(self.event.track_ids), 44)
