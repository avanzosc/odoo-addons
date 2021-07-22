# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo.tests import common


class TestWebsiteEventTrackClaim(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestWebsiteEventTrackClaim, cls).setUpClass()
        cls.wiz_obj = cls.env['wiz.event.participant.create.claim']
        cls.claim_obj = cls.env['crm.claim']
        cls.claim_categ = cls.env['crm.claim.category'].search([], limit=1)
        cond = [('partner_id', '!=', False),
                ('partner_id.parent_id', '!=', False)]
        cls.registration = cls.env['event.registration'].search(cond, limit=1)
        vals = {'partner_id': cls.registration.partner_id.parent_id.id,
                'student_id': cls.registration.partner_id.id,
                'real_date_start': cls.registration.event_id.date_begin.date()}
        cls.registration.write(vals)
        cond = [('event_id', '=', cls.registration.event_id.id)]
        cls.registration.student_id.write({
            'phone': '99999999999',
            'email': '9999@avanzosc.es'})
        cls.track = cls.env['event.track'].search(cond, limit=1)

    def test_website_event_track_claim(self):
        self.assertEqual(self.track.count_registrations, 1)
        result = self.track.button_show_registrations()
        context = result.get('context')
        self.assertEqual(context.get('event_track_id'), self.track.id)
        domain = [('id', 'in', self.registration.student_id.ids)]
        self.assertEqual(result.get('domain'), domain)
        vals = {
            'name': 'test for create claim from wizard',
            'categ_id': self.claim_categ.id,
            'event_track_id': self.track.id,
            'from_session': True}
        wiz = self.wiz_obj.create(vals)
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
