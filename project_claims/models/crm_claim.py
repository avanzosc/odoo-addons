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


class CrmClaim(orm.Model):
    _inherit = 'crm.claim'

    _columns = {
        'project_id': fields.many2one('project.project', 'Project'),
        'task_id': fields.many2one('project.task', 'Task'),
    }

#     def _auto_init(self, cr, context=None):
#         if context is None:
#             context = {}
#         result = super(CrmClaim, self)._auto_init(cr, context=context)
#
#         cr.execute("SELECT id, ref "
#                    "FROM crm_claim "
#                    "WHERE ref LIKE 'project.project,%'")
#
#         results = cr.fetchall()
#         for res in results:
#             project_id = res[1].split(',')[1]
# #             self.write(cr, uid, res[0], {'project_id': project_id},
#                          context=context)
#
#         return result

    def write(self, cr, uid, ids, vals, context=None):
        if context is None:
            context = {}
        if 'ref' in vals:
            if not vals['ref']:
                vals.update({'project_id': False, 'task_id': False})
            else:
                ref = vals['ref'].split(',')
                model = ref[0]
                res_id = ref[1]

                if model == 'project.project':
                    vals.update({'project_id': res_id})
                elif model == 'project.task':
                    vals.update({'task_id': res_id})
                    task = self.pool['project.task'].browse(
                        cr, uid, int(res_id), context=context)
                    if task.project_id:
                        vals.update({'project_id': task.project_id.id})

        return super(CrmClaim, self).write(cr, uid, ids, vals, context=context)
