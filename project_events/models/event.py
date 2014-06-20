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


class EventEvent(orm.Model):
    _inherit = 'event.event'

    def _task_count(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for event in self.browse(cr, uid, ids, context=context):
            res[event.id] = len(event.task_ids)
        return res

    _columns = {
        'project_id': fields.many2one('project.project', 'Project'),
        'task_count': fields.function(_task_count, type='integer',
                                      string='Tasks'),
        'task_ids': fields.many2many('project.task', 'rel_task_event',
                                     'event_id', 'task_id', 'Tasks'),
    }

    def agenda_description(self, cr, uid, ids, context=None):
        if context is None:
            context = {}

        for event in self.browse(cr, uid, ids, context=context):
            if event.task_count > 0:
                agenda = "<p><strong>Agenda:</strong></p>\n<ul>\n"
                for task in event.task_ids:
                    agenda += "<li>" + task.name + "</li>\n"
                agenda += "</ul>\n"

                self.write(cr, uid, event.id,
                           {'description': (event.description or '') + agenda},
                           context=context)
        return True
