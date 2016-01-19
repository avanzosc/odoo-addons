# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestEventProjectFollower(common.TransactionCase):

    def setUp(self):
        super(TestEventProjectFollower, self).setUp()
        self.project_model = self.env['project.project']
        self.event_model = self.env['event.event']
        self.wiz_model = self.env['project.template.wizard']
        project_vals = {'name': 'Project for event 2016-01-20',
                        'date_start': '2016-01-19',
                        'date': '2016-01-20',
                        'use_tasks': True,
                        'members': [(6, 0, [self.ref('base.user_demo')])],
                        'tasks': [(0, 0, {'name': 'Tarea 1'}),
                                  (0, 0, {'name': 'Tarea 2'})]}
        self.project = self.project_model.create(project_vals)

    def test_event_project_follower(self):
        event_vals = {'name': 'Event for project',
                      'date_begin': '2016-01-19',
                      'date_end': '2016-01-20',
                      'project_id': self.project.id}
        event = self.event_model.create(event_vals)
        self.assertIn(
            self.project.members[0].partner_id.id,
            event.message_follower_ids.ids,
            'Partner not found in event followers')
