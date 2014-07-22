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

    def _claim_count(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for project in self.browse(cr, uid, ids, context=context):
            res[project.id] = len(project.claim_ids)
        return res

    _columns = {
        'claim_count': fields.function(_claim_count, type="integer",
                                       string="Claims"),
        'claim_ids': fields.one2many('crm.claim', 'project_id', 'Claims'),
    }


class ProjectTask(orm.Model):
    _inherit = 'project.task'

    def _claim_count(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for task in self.browse(cr, uid, ids, context=context):
            res[task.id] = len(task.claim_ids)
        return res

    _columns = {
        'claim_count': fields.function(_claim_count, type="integer",
                                       string="Claims"),
        'claim_ids': fields.one2many('crm.claim', 'task_id', 'Claims'),
    }
