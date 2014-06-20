# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2008-2014 AvanzOSC S.L. (Oihane) All Rights Reserved
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

from openerp.osv import orm, fields
from datetime import datetime, timedelta


class MeetingFromTask(orm.TransientModel):
    _name = 'project.task.create.meeting'

    _columns = {
        'date': fields.datetime('Date'),
        'duration': fields.float('Duration'),
        'type': fields.many2one('event.type', 'Event Type'),
    }

    _defaults = {
        'date': datetime.now().strftime('%Y-%m-%d 10:00:00'),
        'duration': 4.0,
    }

    def action_meeting(self, cr, uid, ids, context=None):
        if context is None:
            context = {}

        for data in self.browse(cr, uid, ids, context=context):
            projects = {}
            event_ids = []

            event_obj = self.pool['event.event']
            task_obj = self.pool['project.task']
            project_obj = self.pool['project.project']

            task_ids = False
            if 'active_ids' in context:
                task_ids = context['active_ids']

                for task in task_obj.browse(cr, uid, task_ids,
                                            context=context):
                    if task.project_id.id in projects:
                        projects[task.project_id.id].append(task.id)
                    else:
                        projects[task.project_id.id] = [task.id]

            end_date = (datetime.strptime(data.date, '%Y-%m-%d %H:%M:%S') +
                        timedelta(hours=data.duration))
            end_date = end_date.strftime('%Y-%m-%d %H:%M:%S')

            for project_id in projects.keys():
                project = project_obj.browse(cr, uid, project_id,
                                             context=context)
                event_id = event_obj.create(cr, uid,
                                            {
                                                'name': project.name,
                                                'project_id': project_id,
                                                'task_ids':
                                                [[6, 0, projects[project_id]]],
                                                'date_begin': data.date,
                                                'date_end': end_date,
                                                'type': data.type.id or False,
                                            },
                                            context=context)
                event_ids.append(event_id)

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'event.event',
            'view_mode': 'kanban,tree,form',
            'view_type': 'form',
            'target': 'current',
            'domain': [['id', 'in', event_ids]],
            'res_id': event_ids,
        }
