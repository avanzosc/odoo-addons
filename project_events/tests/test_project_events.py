# -*- coding: utf-8 -*-
# (c) 2015 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestProjectEvents(common.TransactionCase):

    def setUp(self):
        super(TestProjectEvents, self).setUp()
        self.project_model = self.env['project.project']
        self.wiz_model = self.env['project.task.create.meeting']
        self.event_model = self.env['event.event']
        task_vals = {'name': 'Task-1 for Project_event'}
        project_vals = {'name': 'Project for event',
                        'use_tasks': True,
                        'members': [(6, 0, [self.ref('base.user_demo')])],
                        'tasks': [(0, 0, task_vals)]}
        self.project = self.project_model.create(project_vals)
        self.wizard = self.wiz_model.create({})
        self.wizard.with_context(
            {'active_ids': [self.project.tasks[0].id]}).action_meeting()

    def test_project_events(self):
        cond = [('project_id', '=', self.project.id)]
        event = self.event_model.search(cond)
        self.assertEqual(
            len(event), 1, 'Event not found for proyect')
        self.assertIn(
            self.project.members[0].partner_id.id,
            event.message_follower_ids.ids,
            'Partner not found in event followers')
