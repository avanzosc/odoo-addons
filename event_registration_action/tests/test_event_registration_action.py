# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo.tests import common


class TestEventRegistationAction(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestEventRegistationAction, cls).setUpClass()
        cls.confirm_obj = cls.env[
            'wiz.event.registration.confirm.participant']
        cls.cancel_obj = cls.env[
            'wiz.event.registration.cancel.participant']
        cls.draft_obj = cls.env[
            'wiz.event.registration.draft.participant']
        cond = [('state', '=', 'draft')]
        cls.registration = cls.env['event.registration'].search(cond, limit=1)

    def test_event_registration_action(self):
        wiz = self.confirm_obj.with_context(
            active_model='event.registration',
            active_ids=self.registration.ids).create({'name': 'a'})
        wiz.action_confirm_participant()
        self.assertEqual(self.registration.state, 'open')
        wiz = self.cancel_obj.with_context(
            active_model='event.registration',
            active_ids=self.registration.ids).create({'name': 'a'})
        wiz.action_cancel_participant()
        self.assertEqual(self.registration.state, 'cancel')
        wiz = self.draft_obj.with_context(
            active_model='event.registration',
            active_ids=self.registration.ids).create({'name': 'a'})
        wiz.action_draft_participant()
        self.assertEqual(self.registration.state, 'draft')
