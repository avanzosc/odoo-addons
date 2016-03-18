# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api


class EventEvent(models.Model):
    _inherit = 'event.event'

    def _compute_event_tasks(self):
        task_obj = self.env['project.task']
        for event in self:
            cond = [('event_id', '=', event.id)]
            tasks = task_obj.search(cond)
            if tasks:
                self.my_task_ids = [(6, 0, tasks.ids)]
            else:
                self.my_task_ids = [(6, 0, [])]

    @api.one
    @api.depends('task_ids')
    def _count_tasks(self):
        self.count_tasks = len(self.my_task_ids)

    my_task_ids = fields.One2many(
        comodel_name='project.task', compute='_compute_event_tasks',
        string='Tasks', oldname='tasks')

    def _create_event_from_sale(self, by_task, sale, line=False):
        project_obj = self.env['project.project']
        cond = [('analytic_account_id', '=', sale.project_id.id)]
        project = project_obj.search(cond, limit=1)
        name = sale.name
        if by_task:
            name = name + ': ' + line.name
        event_vals = sale._prepare_event_data(name, project)
        event = self.with_context(
            sale_order_create_event=True).create(event_vals)
        return event


class EventTrack(models.Model):
    _inherit = 'event.track'

    tasks = fields.Many2many(
        comodel_name="project.task", relation="task_session_project_relation",
        column1="track_id", column2="task_id", copy=False, string="Tasks")


class EventRegistration(models.Model):
    _inherit = 'event.registration'

    @api.multi
    def registration_open(self):
        self.ensure_one()
        tasks = self.env['project.task']
        wiz_obj = self.env['wiz.event.append.assistant']
        result = super(EventRegistration, self).registration_open()
        wiz = wiz_obj.browse(result['res_id'])
        date_from = self.event_id.date_begin
        date_to = self.event_id.date_end
        if self.date_start:
            date_from = self.date_start
        if self.date_end:
            date_to = self.date_end
        sessions = self.event_id.track_ids.filtered(
            lambda x: x.date >= date_from and x.date <= date_to and x.date)
        for session in sessions:
            for task in session.tasks:
                if task not in tasks:
                    tasks += task
        wiz.write({'permitted_tasks': [(6, 0, tasks.ids)],
                   'tasks': [(6, 0, tasks.ids)]})
        return result
