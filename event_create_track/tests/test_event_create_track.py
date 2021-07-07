# Copyright (c) 2021 Berezi Amubieta - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import common, tagged
from odoo import fields


@tagged("post_install", "-at_install")
class TestEventCreateTrack(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestEventCreateTrack, cls).setUpClass()
        date_start = fields.Datetime.from_string('2021-01-04 08:00:00')
        date_end = fields.Datetime.from_string('2021-01-05 10:00:00')
        event_vals = {
            'name': 'aaa',
            'date_begin': date_start,
            'date_end': date_end,
            'resource_calendar_id': cls.env['resource.calendar'].search(
                [], limit=1).id
            }
        cls.event = cls.env['event.event'].create(event_vals)
        cls.stage = cls.env.ref('event.event_stage_announced')

    def test_event_create_track(self):
        self.event.stage_id = self.stage.id
        self.assertEqual(len(self.event.track_ids), 4)
