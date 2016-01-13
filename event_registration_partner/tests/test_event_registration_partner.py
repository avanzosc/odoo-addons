# -*- coding: utf-8 -*-
# (c) 2015 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestEventRegistrationPartner(common.TransactionCase):

    def setUp(self):
        super(TestEventRegistrationPartner, self).setUp()
        self.event_model = self.env['event.event']
        registration_vals = {'partner_id': self.ref('base.res_partner_1'),
                             'nb_register': 1}
        event_vals = {'name': 'Registration partner test',
                      'date_begin': '2016-01-20',
                      'date_end': '2016-01-20',
                      'registration_ids': [(0, 0, registration_vals)]}
        self.event = self.event_model.create(event_vals)

    def test_event_registration_partner(self):
        self.assertEqual(
            len(self.event.registration_ids), 1, 'Event without registrations')
        self.assertIn(
            self.ref('base.res_partner_1'),
            self.event.message_follower_ids.ids,
            'Partner not found in followerw')
