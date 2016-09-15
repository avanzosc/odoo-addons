# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestEventProjectFollower(common.TransactionCase):

    def setUp(self):
        super(TestEventProjectFollower, self).setUp()
        self.project_model = self.env['project.project']
        self.event_model = self.env['event.event']
        partner_model = self.env['res.partner']
        user_model = self.env['res.users']
        partner1 = partner_model.create({
            'name': 'Partner 1',
        })
        self.user1 = user_model.create({
            'partner_id': partner1.id,
            'login': 'user1',
            'password': 'user1',
        })
        partner2 = partner_model.create({
            'name': 'Partner 2',
        })
        self.user2 = user_model.create({
            'partner_id': partner2.id,
            'login': 'user2',
            'password': 'user2',
        })
        project_vals = {'name': 'Project for event 2016-01-20',
                        'date_start': '2016-01-19',
                        'date': '2016-01-20',
                        'use_tasks': True,
                        'calculation_type': 'date_begin',
                        'members': [(6, 0, [self.user1.id,
                                            self.user2.id])],
                        'tasks': [(0, 0, {'name': 'Tarea 1'}),
                                  (0, 0, {'name': 'Tarea 2'})]}
        self.project = self.project_model.create(project_vals)

    def test_event_project_follower_create(self):
        event_vals = {'name': 'Event for project',
                      'date_begin': '2016-01-19',
                      'date_end': '2016-01-20',
                      'project_id': self.project.id}
        event = self.event_model.create(event_vals)
        self.assertTrue(len(self.project.members) > 1)
        self.assertTrue(len(event.message_follower_ids) > 1)
        for member in self.project.members:
            self.assertIn(
                member.partner_id.id,
                event.message_follower_ids.ids,
                'Partner not found in event followers')

    def test_event_project_follower_write(self):
        event_vals = {'name': 'Event for project',
                      'date_begin': '2016-01-19',
                      'date_end': '2016-01-20'}
        event = self.event_model.create(event_vals)
        self.assertTrue(len(self.project.members) > 1)
        self.assertTrue(
            len(self.project.members) != len(event.message_follower_ids))
        event.project_id = self.project
        for member in self.project.members:
            self.assertIn(
                member.partner_id.id,
                event.message_follower_ids.ids,
                'Partner not found in event followers')
