# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo.tests import common


class TestWebsiteEventTrackClaim(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestWebsiteEventTrackClaim, cls).setUpClass()
        cls.wiz_obj = cls.env['wiz.event.participant.create.claim']
        cls.claim_obj = cls.env['crm.claim']
        cls.state_done = cls.env.ref('website_event_track.event_track_stage3')
        cls.state_canceled = cls.env.ref(
            'website_event_track.event_track_stage5')
        cls.claim_categ = cls.env['crm.claim.category'].search([], limit=1)
        for registration in cls.env['event.registration'].search([]):
            if registration.partner_id.parent_id:
                cls.registration = registration
                break
        vals = {'partner_id': cls.registration.partner_id.parent_id.id,
                'student_id': cls.registration.partner_id.id,
                'real_date_start': cls.registration.event_id.date_begin.date()}
        cls.registration.write(vals)
        cond = [('event_id', '=', cls.registration.event_id.id)]
        cls.registration.student_id.write({
            'phone': '99999999999',
            'email': '9999@avanzosc.es'})
        cls.track = cls.env['event.track'].search(cond, limit=1)
        vals = {
            'name': cls.track.partner_id.name,
            'login': cls.track.partner_id.name,
            'password': cls.track.partner_id.name,
            'partner_id': cls.track.partner_id.id}
        cls.user = cls.env['res.users'].create(vals)
        vals = {'name': cls.track.partner_id.name,
                'user_id': cls.user.id}
        cls.env['hr.employee'].create(vals)

    def test_website_event_track_claim(self):
        self.assertEqual(self.track.count_registrations, 1)
        result = self.track.button_show_registrations()
        context = result.get('context')
        self.assertEqual(context.get('event_track_id'), self.track.id)
        domain = [('id', 'in', self.registration.student_id.ids)]
        self.assertEqual(result.get('domain'), domain)
        vals = {
            'categ_id': self.claim_categ.id,
            'event_track_id': self.track.id,
            'from_session': True}
        wiz = self.wiz_obj.create(vals)
        wiz.onchange_categ_id()
        self.assertEqual(wiz.name, self.claim_categ.name)
        wiz.with_context(
            active_ids=self.registration.student_id.ids).action_create_claim()
        self.assertEqual(self.track.count_claims, 1)
        cond = [('event_track_id', '=', self.track.id)]
        claim = self.claim_obj.search(cond, limit=1)
        domain = [('id', 'in', claim.ids)]
        result = self.track.button_show_claims()
        self.assertEqual(result.get('domain'), domain)
        self.assertEqual(self.track.event_id.count_claims, 1)
        result = self.track.event_id.button_show_claims()
        self.assertEqual(result.get('domain'), domain)
        self.track.button_session_done()
        self.assertEqual(self.track.stage_id.id, self.state_done.id)
        self.track.button_session_cancel()
        self.assertEqual(self.track.stage_id.id, self.state_canceled.id)
