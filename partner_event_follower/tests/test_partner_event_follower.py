# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp.tests.common import TransactionCase


class TestPartnerEventFollower(TransactionCase):

    def setUp(self):
        super(TestPartnerEventFollower, self).setUp()
        self.event_model = self.env['event.event']
        self.event_0 = self.env.ref('event.event_0')
        self.event_0.create_partner = True
        registration_model = self.env['event.registration']
        partner_model = self.env['res.partner']
        self.partner_01 = partner_model.create({'name': 'Test Partner 01',
                                                'email': 'email01@test.com'})
        self.registration_01 = registration_model.create({
            'email': 'email01@test.com', 'event_id': self.event_0.id})
        self.registration_02 = registration_model.create({
            'email': 'email02@test.com', 'event_id': self.event_0.id,
            'name': 'Test Registration 02', 'phone': '254728911'})

    def test_create(self):
        self.assertEqual(self.partner_01.name, self.registration_01.name)
        self.assertEqual(self.partner_01.email, self.registration_01.email)
        self.assertEqual(self.partner_01.phone, self.registration_01.phone)
        partner_02 = self.registration_02.partner_id
        self.assertEqual(partner_02.name, self.registration_02.name)
        self.assertEqual(partner_02.email, self.registration_02.email)
        self.assertEqual(partner_02.phone, self.registration_02.phone)

    def test_count_registrations(self):
        event_1 = self.env.ref('event.event_1')
        registration_model = self.env['event.registration']
        registration_03 = registration_model.create({
            'event_id': event_1.id, 'partner_id': self.partner_01.id})
        self.assertEqual(self.partner_01.event_count, 0)
        registration_03.state = 'done'
        self.assertEqual(self.partner_01.event_count, 1)

    def test_button_register(self):
        event_1 = self.env.ref('event.event_1')
        wizard = self.env['res.partner.register.event'].create({
            'event': event_1.id})
        active_ids = [self.partner_01.id, self.registration_02.partner_id.id]
        wizard.with_context({'active_ids': active_ids}).button_register()

    def test_event_followers(self):
        registration_vals = {'partner_id': self.ref('base.res_partner_1'),
                             'nb_register': 1}
        event_vals = {'name': 'Registration partner test',
                      'date_begin': '2016-01-20',
                      'date_end': '2016-01-20',
                      'registration_ids': [(0, 0, registration_vals)]}
        event = self.event_model.create(event_vals)
        self.assertEqual(
            len(event.registration_ids), 1, 'Event  without registrations')
        self.assertIn(
            self.ref('base.res_partner_1'),
            event.message_follower_ids.ids,
            'Partner not found in followerw')
