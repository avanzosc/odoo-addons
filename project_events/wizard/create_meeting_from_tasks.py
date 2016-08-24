# -*- coding: utf-8 -*-
##############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

from openerp import api, fields, models
from datetime import timedelta


class MeetingFromTask(models.TransientModel):
    _name = 'project.task.create.meeting'

    date = fields.Datetime(string='Date', default=lambda w: w._default_date())
    duration = fields.Float(string='Duration', default=4.0)
    type = fields.Many2one(comodel_name='event.type', string='Event Type')

    @api.model
    def _default_date(self):
        return fields.Datetime.from_string(
            fields.Datetime.now()).replace(hour=8, minute=0, second=0)

    @api.multi
    def action_meeting(self):
        for data in self:
            projects = {}
            event_ids = []
            event_obj = self.env['event.event']
            task_obj = self.env['project.task']
            project_obj = self.env['project.project']
            task_ids = self.env.context.get('active_ids')
            for task in task_obj.browse(task_ids):
                if task.project_id.id in projects:
                    projects[task.project_id.id].append(task.id)
                else:
                    projects[task.project_id.id] = [task.id]
            end_date = fields.Datetime.to_string(
                fields.Datetime.from_string(data.date) +
                timedelta(hours=data.duration))
            for project_id in projects.keys():
                project = project_obj.browse(project_id)
                event = event_obj.create({
                    'name': project.name,
                    'project_id': project_id,
                    'task_ids': [(6, 0, projects[project_id])],
                    'date_begin': data.date,
                    'date_end': end_date,
                    'type': data.type.id or False,
                })
                event_ids.append(event.id)
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'event.event',
            'view_mode': 'kanban,tree,form',
            'view_type': 'form',
            'target': 'current',
            'domain': [['id', 'in', event_ids]],
            'res_id': event_ids,
        }
