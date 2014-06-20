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


class ProjectProject(orm.Model):
    _inherit = 'project.project'

    def _meeting_count(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for project in self.browse(cr, uid, ids, context=context):
            res[project.id] = len(project.meeting_ids)
        return res

    _columns = {
        'meeting_count': fields.function(_meeting_count, type='integer',
                                         string='Meetings'),
        'meeting_ids': fields.one2many('event.event', 'project_id',
                                       'Meetings'),
    }


class ProjectTask(orm.Model):
    _inherit = 'project.task'

    def _meeting_count(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for task in self.browse(cr, uid, ids, context=context):
            res[task.id] = len(task.meeting_ids)
        return res

    def _pending_meeting_count(self, cr, uid, ids, field_name, arg,
                               context=None):
        res = {}
        for task in self.browse(cr, uid, ids, context=context):
            meeting_cnt = 0
            for meeting in task.meeting_ids:
                if meeting.state in ('draft', 'confirm'):
                    meeting_cnt += 1
            res[task.id] = meeting_cnt
        return res

    _columns = {
        'meeting_count': fields.function(_meeting_count, type='integer',
                                         string='Meetings'),
        'pending_meeting_count': fields.function(_pending_meeting_count,
                                                 type='integer',
                                                 string='Pending Meetings'),
        'meeting_ids': fields.many2many('event.event', 'rel_task_event',
                                        'task_id', 'event_id', 'Tasks'),
    }

    def action_show_meetings(self, cr, uid, ids, context=None):
        if context is None:
            context = {}

        meeting_ids = self.pool['event.event'].search(cr, uid,
                                                      [['task_ids',
                                                        'in',
                                                        ids]])

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'event.event',
            'view_mode': 'kanban,tree,calendar,form',
            'view_type': 'form',
            'target': 'current',
            'domain': [['id', 'in', meeting_ids]],
            'res_id': meeting_ids,
        }
