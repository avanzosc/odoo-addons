# -*- coding: utf-8 -*-
# (c) 2016 Mikel Arregi - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestProjectEventsOperations(common.TransactionCase):

    def setUp(self):
        super(TestProjectEventsOperations, self).setUp()
        self.project_model = self.env['project.project']
        self.event_model = self.env['event.event']
        self.wiz_copy_model = self.env['events.copy']
        self.wiz_date_model = self.env['events.date.modify']
        self.wiz_unifi_model = self.env['events.time.modify']
        project_vals = {'name': 'project procurement service project',
                        'calculation_type': 'date_begin',
                        'date_start': '2016-03-01',
                        'date': '2016-03-31'}
        self.project = self.project_model.create(project_vals)
        self.project2 = self.project_model.create(project_vals)
        event_vals = {'name': 'event for project copy',
                      'date_begin': '2016-03-05 00:00:00',
                      'date_end': '2016-03-31 00:00:00',
                      'project_id': self.project2.id}
        self.event = self.event_model.create(event_vals)

    def test_project_events_operations(self):
        wiz_vals = {'project_id': self.project.id}
        event_copy = self.wiz_copy_model.create(wiz_vals)
        event_copy.with_context(
            {'active_ids': [self.event.id]}).copy_events()
        cond = [('name', '=', self.event.name),
                ('id', '>', self.event.id)]
        new_event = self.event_model.search(cond)
        self.assertNotEqual(
            len(new_event), 0, 'New event not found')

    def test_project_events_operations_date_modifi(self):
        self.event.project_id.date_start = '2016-03-01'
        self.event.project_id.date = '2016-03-31'
        self.event.date_begin = '2016-03-05 00:00:00'
        self.event.date_end = '2016-03-31 00:00:00'
        old_date_begin = self.event.date_begin
        wiz_vals = {'forward': False,
                    'qty': 5,
                    'measure': 'months'}
        wiz = self.wiz_date_model.create(wiz_vals)
        wiz.with_context({'active_ids': [self.event.id]}).modify_date()
        self.assertNotEqual(
            old_date_begin, self.event.date_begin, 'Date not modified')

    def test_project_events_operations_timetable_unifi(self):
        old_date_begin = self.event.date_begin
        wiz_vals = {'start_time': '2016-02-28 05:00:00',
                    'qty': 5}
        wiz = self.wiz_unifi_model.create(wiz_vals)
        wiz.with_context({'active_ids': [self.event.id]}).change_time()
        self.assertNotEqual(
            old_date_begin, self.event.date_begin, 'Datetime not modified')
