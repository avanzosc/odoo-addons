# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestEventTrackAssistant(common.TransactionCase):

    def setUp(self):
        super(TestEventTrackAssistant, self).setUp()
        self.event_model = self.env['event.event']
        self.wiz_add_model = self.env['wiz.event.append.assistant']
        self.wiz_del_model = self.env['wiz.event.delete.assistant']
        event_vals = {'name': 'Registration partner test',
                      'date_begin': '2016-01-20',
                      'date_end': '2016-01-31',
                      'track_ids': [(0, 0, {'name': 'sesion 1'}),
                                    (0, 0, {'name': 'sesion 2',
                                            'date': '2016-01-22'}),
                                    (0, 0, {'name': 'sesion 4',
                                            'date': '2016-01-25'}),
                                    (0, 0, {'name': 'sesion 4',
                                            'date': '2016-01-28'})]}
        self.event = self.event_model.create(event_vals)

    def test_event_track_assistant(self):
        wiz_vals = {'from_date': '2016-01-20',
                    'to_date': '2016-01-31',
                    'partner': self.env.ref('base.res_partner_25').id}
        wiz = self.wiz_add_model.create(wiz_vals)
        wiz.with_context({'active_ids': [self.event.id]}).action_append()
        self.assertEqual(
            len(self.event.registration_ids), 1,
            'Not registration found for event')
        self.assertEqual(
            self.event.registration_ids[0].partner_id.id,
            self.ref('base.res_partner_25'),
            'Not partner found in registration')
        self.assertIn(
            self.event.registration_ids[0].id,
            self.event.track_ids[0].registrations.ids,
            'Partner not found in sesion')

    def test_event_sessions_delete_past_and_later_date(self):
        wiz_vals = {'from_date': '2016-01-20',
                    'to_date': '2016-01-31',
                    'partner': self.env.ref('base.res_partner_25').id}
        wiz = self.wiz_add_model.create(wiz_vals)
        wiz.with_context({'active_ids': [self.event.id]}).action_append()
        wiz_vals = {'from_date': '2016-01-24',
                    'to_date': '2016-01-27',
                    'partner': self.env.ref('base.res_partner_25').id}
        wiz = self.wiz_del_model.create(wiz_vals)
        wiz.with_context(
            {'active_ids': [self.event.id]}).onchange_information()
        wiz.with_context(
            {'active_ids': [self.event.id]}).action_delete_past_and_later()
        self.assertEqual(
            len(self.env.ref('base.res_partner_25').sessions),
            0, 'Not partner found in registration')

    def test_event_sessions_nodelete_past_and_later_date(self):
        wiz_vals = {'from_date': '2016-01-20',
                    'to_date': '2016-01-31',
                    'partner': self.env.ref('base.res_partner_25').id}
        wiz = self.wiz_add_model.create(wiz_vals)
        wiz.with_context({'active_ids': [self.event.id]}).action_append()
        wiz_vals = {'from_date': '2016-01-24',
                    'to_date': '2016-01-27',
                    'partner': self.env.ref('base.res_partner_25').id}
        wiz = self.wiz_del_model.create(wiz_vals)
        wiz.with_context(
            {'active_ids': [self.event.id]}).onchange_information()
        wiz.with_context(
            {'active_ids': [self.event.id]}).action_nodelete_past_and_later()
        self.assertEqual(
            len(self.env.ref('base.res_partner_25').sessions),
            2, 'No sessions found for partner')
