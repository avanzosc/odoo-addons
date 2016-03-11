# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestEventTrackAssistant(common.TransactionCase):

    def setUp(self):
        super(TestEventTrackAssistant, self).setUp()
        self.event_model = self.env['event.event']
        self.registration_model = self.env['event.registration']
        self.wiz_add_model = self.env['wiz.event.append.assistant']
        self.wiz_del_model = self.env['wiz.event.delete.assistant']
        event_vals = {'name': 'Registration partner test',
                      'date_begin': '2016-01-20',
                      'date_end': '2016-01-31',
                      'track_ids': [(0, 0, {'name': 'sesion 2',
                                            'date': '2016-01-22 00:00:00'}),
                                    (0, 0, {'name': 'sesion 4',
                                            'date': '2016-01-25 00:00:00'}),
                                    (0, 0, {'name': 'sesion 4',
                                            'date': '2016-01-28 00:00:00'})]}
        self.event = self.event_model.create(event_vals)

    def test_event_track_assistant(self):
        self.event.date_begin = '2016-01-24 00:00:00'
        self.event.onchange_date_begin()
        self.event.date_end = '2016-01-26 00:00:00'
        self.event.onchange_date_end()
        self.event.date_begin = '2016-01-20 00:00:00'
        self.event.date_end = '2016-01-31 00:00:00'
        wiz_vals = {'min_event': self.event.id,
                    'max_event': self.event.id,
                    'min_from_date': '2016-01-20 00:00:00',
                    'max_to_date': '2016-01-31 00:00:00',
                    'from_date': '2016-01-20',
                    'to_date': '2016-01-31',
                    'partner': self.env.ref('base.res_partner_26').id}
        wiz = self.wiz_add_model.create(wiz_vals)
        wiz.with_context({'active_ids': [self.event.id]}).action_append()
        self.assertEqual(
            len(self.event.registration_ids), 1,
            'Not registration found for event')
        self.assertEqual(
            self.event.registration_ids[0].partner_id.id,
            self.ref('base.res_partner_26'),
            'Not partner found in registration')
        self.event.track_ids[0].write({'date': '2016-01-20 00:00:00',
                                       'real_duration': 5.0})
        self.event.track_ids[0]._compute_real_date_end()
        wiz.from_date = '2016-05-01'
        wiz.onchange_dates_and_partner()
        wiz.write({'from_date': '2016-01-20',
                   'to_date': '2016-01-15'})
        wiz.onchange_dates_and_partner()
        wiz.write({'from_date': '2016-01-01',
                   'to_date': '2016-01-31'})
        wiz.onchange_dates_and_partner()
        wiz.write({'from_date': '2016-01-01',
                   'min_from_date': '2016-01-20'})
        wiz.onchange_dates_and_partner()
        wiz.write({'from_date': '2016-01-31',
                   'max_to_date': '2016-01-25'})
        wiz.onchange_dates_and_partner()
        wiz.write({'to_date': '2016-01-01',
                   'min_from_date': '2016-01-20'})
        wiz.onchange_dates_and_partner()
        wiz.write({'to_date': '2016-01-31',
                   'max_to_date': '2016-01-20'})
        wiz.onchange_dates_and_partner()
        wiz_vals = {'from_date': '2016-01-20',
                    'to_date':  '2016-01-31',
                    'partner': self.env.ref('base.res_partner_26').id}
        wiz = self.wiz_add_model.create(wiz_vals)
        wiz.with_context({'active_ids': [self.event.id]}).action_append()
        sessions = self.event.track_ids[0].presences.filtered(
            lambda x: x.partner.id ==
            self.event.registration_ids[0].partner_id.id)
        sessions[0]._catch_session_date()
        sessions[0]._catch_session_duration()
        sessions[0]._catch_name()
        sessions[0]._catch_event()
        sessions[0]._get_allowed_partners()
        sessions[0].onchange_session()
        sessions[0].button_completed()
        sessions[0].button_canceled()
        sessions[0].partner._count_session()
        sessions[0].partner._count_presences()
        sessions[0].partner.show_sessions_from_partner()
        sessions[0].partner.show_presences_from_partner()
        self.event.registration_ids[0].unlink()
        self.event.registration_ids[0].date_start = '2016-01-22 00:00:00'
        self.event.registration_ids[0].date_end = '2016-01-28 00:00:00'
        self.event.registration_ids[0].registration_open()
        self.event.registration_ids[0].button_reg_cancel()
        self.assertNotEqual(
            len(sessions), 0, 'Partner not found in session')
        wiz_vals = {'registration': self.event.registration_ids[0].id,
                    'min_event': self.event.id,
                    'max_event': self.event.id,
                    'min_from_date': '2016-01-20 00:00:00',
                    'max_to_date': '2016-01-31 00:00:00',
                    'from_date': '2016-01-20',
                    'to_date': '2016-01-31',
                    'partner': self.env.ref('base.res_partner_26').id}
        wiz = self.wiz_add_model.create(wiz_vals)
        self.event.registration_ids[0].state = 'open'
        wiz.with_context(
            {'active_ids': [self.event.id]}).onchange_dates_and_partner()
        wiz.with_context({'active_ids': [self.event.id]}).action_append()
        self.event.registration_ids[0].date_start = '2016-01-01 00:00:00'
        self.event.date_begin = '2016-01-02 00:00:00'
        self.event.registration_ids[0].onchange_date_start_date_end()
        self.event.registration_ids[0].date_start = '2016-01-30 00:00:00'
        self.event.date_end = '2016-01-28 00:00:00'
        self.event.registration_ids[0].onchange_date_start_date_end()
        self.event.registration_ids[0].date_end = '2016-01-30 00:00:00'
        self.event.date_end = '2016-01-28 00:00:00'
        self.event.registration_ids[0].onchange_date_start_date_end()
        self.event.registration_ids[0].date_end = '2016-01-25 00:00:00'
        self.event.date_begin = '2016-01-28 00:00:00'
        self.event.registration_ids[0].onchange_date_start_date_end()
        self.event.registration_ids[0].date_start = False
        self.event.registration_ids[0].date_end = False
        self.event.registration_ids[0].onchange_date_start_date_end()

    def test_event_sessions_delete_past_and_later_date(self):
        wiz_vals = {'min_event': self.event.id,
                    'max_event': self.event.id,
                    'min_from_date': '2016-01-20',
                    'max_to_date': '2016-01-31',
                    'from_date': '2016-01-20',
                    'to_date': '2016-01-31',
                    'partner': self.env.ref('base.res_partner_26').id}
        wiz = self.wiz_add_model.create(wiz_vals)
        wiz.with_context({'active_ids': [self.event.id]}).action_append()
        wiz_vals = {'min_event': self.event.id,
                    'max_event': self.event.id,
                    'min_from_date': '2016-01-20',
                    'max_to_date': '2016-01-31',
                    'from_date': '2016-01-24',
                    'to_date': '2016-01-27',
                    'partner': self.env.ref('base.res_partner_26').id}
        wiz = self.wiz_del_model.create(wiz_vals)
        wiz.with_context(
            {'active_ids': [self.event.id]}).onchange_information()
        vals = ['max_event', 'max_to_date', 'min_from_date', 'min_event',
                'from_date', 'later_sessions', 'past_sessions', 'partner',
                'message', 'to_date']
        wiz.with_context(
            {'active_ids': [self.event.id]}).default_get(vals)
        wiz.from_date = '2016-05-01'
        wiz._dates_control()
        wiz.write({'from_date': '2016-01-20',
                   'to_date': '2016-01-15'})
        wiz._dates_control()
        wiz.write({'from_date': '2016-01-01',
                   'to_date': '2016-01-31'})
        wiz._dates_control()
        wiz.write({'from_date': '2016-01-01',
                   'min_from_date': '2016-01-20'})
        wiz._dates_control()
        wiz.write({'from_date': '2016-01-31',
                   'max_to_date': '2016-01-25'})
        wiz._dates_control()
        wiz.write({'to_date': '2016-01-01',
                   'min_from_date': '2016-01-20'})
        wiz._dates_control()
        wiz.write({'to_date': '2016-01-31',
                   'max_to_date': '2016-01-20'})
        wiz._dates_control()
        wiz.write({'min_from_date': '2016-01-20',
                   'max_to_date': '2016-01-31',
                   'from_date': '2016-01-20',
                   'to_date': '2016-01-31'})
        wiz.with_context(
            {'active_ids': [self.event.id]}).action_nodelete_past_and_later()
        sessions = self.env.ref('base.res_partner_26').sessions
        wiz.with_context(
            {'active_ids':
             [self.event.id]})._delete_registrations_between_dates(sessions)
        wiz.with_context(
            {'active_ids': [self.event.id]}).action_delete_past_and_later()
        self.assertNotEqual(
            len(self.env.ref('base.res_partner_26').sessions),
            0, 'Not partner found in registration')
        wiz_vals = {'min_event': self.event.id,
                    'max_event': self.event.id,
                    'min_from_date': '2016-01-20',
                    'max_to_date': '2016-01-31',
                    'from_date': '2016-01-20',
                    'to_date': '2016-01-31',
                    'partner': self.env.ref('base.res_partner_26').id}
        wiz = self.wiz_add_model.create(wiz_vals)
        wiz.with_context({'active_ids': [self.event.id]}).action_append()
        wiz_vals = {'min_event': self.event.id,
                    'max_event': self.event.id,
                    'min_from_date': '2016-01-20',
                    'max_to_date': '2016-01-31',
                    'from_date': '2016-01-20',
                    'to_date': '2016-01-31',
                    'partner': self.env.ref('base.res_partner_26').id}
        wiz = self.wiz_add_model.create(wiz_vals)
        wiz.onchange_dates_and_partner()
        wiz_vals = {'min_event': self.event.id,
                    'max_event': self.event.id,
                    'registration': self.event.registration_ids[0].id,
                    'min_from_date': '2016-01-20',
                    'max_to_date': '2016-01-31',
                    'from_date': '2016-01-24',
                    'to_date': '2016-01-27',
                    'partner': self.env.ref('base.res_partner_26').id}
        wiz = self.wiz_del_model.create(wiz_vals)
        wiz.onchange_information()

    def test_event_sessions_withous_registration(self):
        registration_vals = ({'event_id': self.event.id,
                              'partner_id':
                              self.env.ref('base.res_partner_26').id,
                              'state': 'draft'})
        registration = self.registration_model.create(registration_vals)
        registration._onchange_partner()
        wiz_vals = {'min_event': self.event.id,
                    'max_event': self.event.id,
                    'min_from_date': '2016-01-20',
                    'max_to_date': '2016-01-31',
                    'from_date': '2016-01-20',
                    'to_date': '2016-01-31',
                    'partner': self.env.ref('base.res_partner_26').id}
        wiz = self.wiz_add_model.create(wiz_vals)
        wiz.with_context(
            {'active_ids': [self.event.id]}).onchange_dates_and_partner()
        wiz._update_create_registration(self.event, [registration])
        wiz.update({'from_date': '2016-01-10'})
        registration.date_start = '2016-01-20 00:00:00'
        registration.event_id.date_begin = '2016-01-05'
        wiz._compute_update_registration_start_date(registration)
        wiz.update({'to_date': '2016-03-30'})
        registration.date_end = '2016-01-15 00:00:00'
        registration.event_id.date_end = '2016-01-20 00:00:00'
        wiz._compute_update_registration_end_date(registration)
