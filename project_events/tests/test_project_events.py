# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestProjectEvents(common.TransactionCase):

    def setUp(self):
        super(TestProjectEvents, self).setUp()
        self.project_model = self.env['project.project']
        self.event_model = self.env['event.event']
        self.wiz_model = self.env['project.task.create.meeting']
        project_vals = {
            'name': 'project for project events',
            'use_task': True,
            'date_start': '2016-02-28',
            'tasks': [(0, 0, {'name': 'Tarea 1'}),
                      (0, 0, {'name': 'Tarea 2'})]}
        self.project = self.project_model.create(project_vals)

    def test_project_event(self):
        task = self.project.tasks[0]
        wiz_vals = {'date': '2016-03-05',
                    'duration': 4.0,
                    'type': self.ref('project_events.meeting_type')}
        wiz = self.wiz_model.create(wiz_vals)
        wiz.with_context({'active_ids': [task.id]}).action_meeting()
        self.assertNotEqual(
            task.meeting_count, 0, 'Meeting not created for task')
        self.assertNotEqual(
            task.pending_meeting_count, 0, 'Pending Meeting not found')
        self.assertNotEqual(
            self.project.meeting_count, 0, 'Meeting not found in project')
        self.assertNotEqual(
            self.project.meeting_count, 0, 'Meeting not found in project')
        cond = [('name', '=', self.project.name),
                ('project_id', '=', self.project.id)]
        event = self.event_model.search(cond, limit=1)
        self.assertNotEqual(
            event.task_count, 0, 'Meeting without task')
