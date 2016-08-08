# -*- coding: utf-8 -*-
# © 2014-2016 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, fields, models


class CrmClaim(models.Model):
    _inherit = 'crm.claim'

    project_id = fields.Many2one(
        comodel_name='project.project', string='Project')
    task_id = fields.Many2one(
        comodel_name='project.task', string='Task')

    @api.multi
    def write(self, vals):
        if vals.get('ref', False):
            ref = vals['ref'].split(',')
            model = ref[0]
            res_id = ref[1]
            if model == 'project.project' and 'project_id' not in vals:
                vals.update({'project_id': res_id})
            elif model == 'project.task' and 'task_id' not in vals:
                vals.update({'task_id': res_id})
                task = self.env['project.task'].browse(int(res_id))
                if task.project_id:
                    vals.update({'project_id': task.project_id.id})
        elif vals.get('task_id', False):
            vals['ref'] = 'project.task,%s' % vals['task_id']
        elif vals.get('project_id', False):
            vals['ref'] = 'project.project,%s' % vals['project_id']
        return super(CrmClaim, self).write(vals)

    @api.onchange('project_id')
    def onchange_project_id(self):
        if self.task_id and self.task_id.project_id != self.project_id:
            self.task_id = False
        return {'domain':
                {'task_id': [('project_id', '=', self.project_id.id)]}}

    @api.onchange('task_id')
    def onchange_task_id(self):
        if self.task_id:
            self.project_id = self.task_id.project_id
