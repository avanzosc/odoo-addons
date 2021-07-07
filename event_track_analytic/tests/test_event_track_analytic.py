# Copyright (c) 2021 Berezi Amubieta - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import common, tagged
from odoo import fields


@tagged("post_install", "-at_install")
class TestEventTrackAnalytic(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestEventTrackAnalytic, cls).setUpClass()
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
        cls.event.stage_id = cls.stage.id
        cond = [('is_done', '=', True)]
        cls.track_done_state = cls.env['event.track.stage'].search(
            cond, limit=1)

    def test_event_create_track(self):
        self.event.track_ids[0].stage_id = self.track_done_state.id
        self.assertEqual(
            len(self.event.track_ids[0].account_analytic_line_ids), 1)
