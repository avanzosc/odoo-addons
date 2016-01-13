# -*- coding: utf-8 -*-
# (c) 2015 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models, api
from datetime import datetime, timedelta


class MeetingFromTask(models.TransientModel):
    _name = 'project.task.create.meeting'

    date = fields.Datetime(
        string='Date', default=fields.Datetime.now())
    duration = fields.Float(
        string='Duration', default=4.0)
    type = fields.Many2one('event.type', string='Event Type')

    @api.multi
    def action_meeting(self):
        self.ensure_one()
        projects = {}
        event_ids = []
        event_obj = self.env['event.event']
        task_obj = self.env['project.task']
        project_obj = self.env['project.project']
        if 'active_ids' in self.env.context:
            for task in task_obj.browse(self.env.context.get('active_ids')):
                if task.project_id.id in projects:
                    projects[task.project_id.id].append(task.id)
                else:
                    projects[task.project_id.id] = [task.id]
        end_date = (datetime.strptime(self.date, '%Y-%m-%d %H:%M:%S') +
                    timedelta(hours=self.duration))
        end_date = end_date.strftime('%Y-%m-%d %H:%M:%S')
        for project_id in projects.keys():
            project = project_obj.browse(project_id)
            event_id = event_obj.create({'name': project.name,
                                         'project_id': project_id,
                                         'task_ids':
                                         [[6, 0, projects[project_id]]],
                                         'date_begin': self.date,
                                         'date_end': end_date,
                                         'type': self.type.id or False})
            event_ids.append(event_id.id)
        return {'type': 'ir.actions.act_window',
                'res_model': 'event.event',
                'view_mode': 'kanban,tree,form',
                'view_type': 'form',
                'target': 'current',
                'domain': [['id', 'in', event_ids]],
                'res_id': event_ids}
