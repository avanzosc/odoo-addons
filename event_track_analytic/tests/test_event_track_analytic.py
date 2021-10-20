# Copyright (c) 2021 Berezi Amubieta - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import common, tagged


@tagged("post_install", "-at_install")
class TestEventTrackAnalytic(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestEventTrackAnalytic, cls).setUpClass()
        vals = {'name': 'User event track analytic',
                'login': 'usereventrackanalytic@avanzosc.es'}
        cls.user = cls.env['res.users'].create(vals)
        vals = {'name': 'Employee Event Track Analytic',
                'user_id': cls.user.id}
        cls.employee = cls.env['hr.employee'].create(vals)
        cond = [('is_done', '=', True)]
        cls.track_done_state = cls.env['event.track.stage'].search(
            cond, limit=1)
        track = cls.env['event.track'].search(
            [('stage_id.name', '=', 'Confirmed')], limit=1)
        cls.event = track.event_id
        cls.event.track_ids[0].partner_id = cls.user.partner_id.id

    def test_event_create_track(self):
        self.event.track_ids[0].stage_id = self.track_done_state.id
        self.assertEqual(
            len(self.event.track_ids[0].account_analytic_line_ids), 1)
