# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestProjectEventsCopy(common.TransactionCase):

    def setUp(self):
        super(TestProjectEventsCopy, self).setUp()
        self.project_model = self.env['project.project']
        self.event_model = self.env['event.event']
        self.wiz_model = self.env['project.task.create.meeting']
        self.event_copy_model = self.env['events.copy']
        project_vals = {
            'name': 'project for project events',
            'calculation_type': 'date_begin',
            'date_start': '2016-02-28',
            'tasks': [(0, 0, {'name': 'Tarea 1'}),
                      (0, 0, {'name': 'Tarea 2'})]}
        self.project = self.project_model.create(project_vals)
        event_vals = {'name': 'event for project copy',
                      'date_begin': '2016-02-28',
                      'date_end': '2016-03-31'}
        self.event = self.event_model.create(event_vals)

    def test_project_events_copy(self):
        task = self.project.tasks[0]
        wiz_vals = {'date': '2016-02-28',
                    'duration': 4.0,
                    'type': self.ref('project_events.meeting_type')}
        wiz = self.wiz_model.create(wiz_vals)
        wiz.with_context({'active_ids': [task.id]}).action_meeting()
        cond = [('name', '=', self.project.name),
                ('project_id', '=', self.project.id)]
        event = self.event_model.search(cond, limit=1)
        event.agenda_description()
        wiz.with_context({'active_ids': [task.id]}).action_meeting()
        wiz_vals = {'project_id': self.project.id,
                    'start_date': '2016-05-01'}
        event_copy = self.event_copy_model.create(wiz_vals)
        event_copy.with_context(
            {'active_ids': [self.event.id]}).copy_events()
        cond = [('name', '=', self.event.name),
                ('id', '>', self.event.id)]
        new_event = self.event_model.search(cond)
        new_event.agenda_description()
        self.assertNotEqual(
            len(new_event), 0, 'New event not found')
