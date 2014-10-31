# -*- encoding: utf-8 -*-
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

from openerp.osv import orm, fields


class ProjectTaskDelegate(orm.TransientModel):
    _inherit = 'project.task.delegate'

    _columns = {
        'split_in': fields.integer('Split in'),
        'task_planned_hours': fields.float('Planned Hours'),
        'task_planned_hours_me': fields.float('Hours to Validate'),
    }

    _defaults = {
        'split_in': 1,
    }

    def default_get(self, cr, uid, fields, context=None):
        res = super(ProjectTaskDelegate, self).default_get(cr, uid, fields,
                                                           context=context)

        if context is None:
            context = {}
        record_id = context.get('active_id', False)
        if not record_id:
            return res
        task_obj = self.pool['project.task']
        task = task_obj.browse(cr, uid, record_id, context=context)

        if 'task_planned_hours' in fields:
            res['task_planned_hours'] = task.planned_hours or 0.0
        return res

    def onchange_split_in(self, cr, uid, ids, split_in, task_planned_hours,
                          planned_hours_me, context=None):
        task_planned_hours_me = planned_hours_me * split_in
        planned = (task_planned_hours / split_in) - planned_hours_me

        value = {
            'planned_hours': planned,
            'task_planned_hours_me': task_planned_hours_me,
        }

        return {'value': value}
