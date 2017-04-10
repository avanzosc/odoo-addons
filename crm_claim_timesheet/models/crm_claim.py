# -*- coding: utf-8 -*-
# (Copyright) 2017 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, fields, models


class CrmClaim(models.Model):
    _inherit = 'crm.claim'

    analytic_id = fields.Many2one(
        comodel_name='account.analytic.account', string='Analytic account',
        related='project_id.analytic_account_id', store=True)
    use_timesheets = fields.Boolean(
        related='analytic_id.use_timesheets', store=True)
    timesheet_ids = fields.One2many(
        comodel_name='hr.analytic.timesheet', string='Timesheets',
        inverse_name='claim_id')

    @api.onchange('analytic_id')
    def onchange_analytic_id(self):
        for line in self.filtered(lambda x: x.analytic_id):
            line.timesheet_ids = line.analytic_id.timesheet_ids

    @api.onchange('task_id')
    def onchange_task_id(self):
        for line in self:
            if line.task_id:
                try:
                    line.timesheet_ids = \
                        line.analytic_id.timesheet_ids.filtered(
                            lambda x: x.task_id == line.task_id)
                except:
                    continue
            else:
                line.timesheet_ids = line.analytic_id.timesheet_ids
