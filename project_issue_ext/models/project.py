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


class ProjectTask(orm.Model):
    _inherit = 'project.task'

    def _issue_count(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for task in self.browse(cr, uid, ids, context=context):
            res[task.id] = len(task.issue_ids)
        return res

    _columns = {
        'issue_count': fields.function(_issue_count, type='integer',
                                       string='Issues'),
        'issue_ids': fields.one2many('project.issue', 'task_id', 'Issues'),
    }

    def action_show_issues(self, cr, uid, ids, context=None):
        if context is None:
            context = {}

        issue_obj = self.pool['project.issue']
        issue_ids = issue_obj.search(cr, uid, [['task_id', 'in', ids]],
                                     context=context)
        task = self.browse(cr, uid, ids, context=context)

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'project.issue',
            'view_mode': 'kanban,tree,calendar,form',
            'view_type': 'form',
            'target': 'current',
            'domain': [['id', 'in', issue_ids]],
            'res_id': issue_ids,
            'context': {'default_project_id': task[0].project_id.id,
                        'default_task_id': ids[0]}
        }
