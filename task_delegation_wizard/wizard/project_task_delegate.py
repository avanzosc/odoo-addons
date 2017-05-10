# -*- coding: utf-8 -*-
# (c) 2016 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
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

    def default_get(self, cr, uid, var_fields, context=None):
        res = super(ProjectTaskDelegate, self).default_get(cr, uid, var_fields,
                                                           context=context)
        if context is None:
            context = {}
        record_id = context.get('active_id', False)
        if not record_id:
            return res
        task_obj = self.pool['project.task']
        task = task_obj.browse(cr, uid, record_id, context=context)
        if 'task_planned_hours' in var_fields:
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
