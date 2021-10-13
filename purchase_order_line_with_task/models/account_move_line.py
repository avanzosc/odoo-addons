# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, api


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    allowed_task_ids = fields.Many2many(
        string='Allowed tasks', comodel_name='project.task')
    task_id = fields.Many2one(
        string='Task', comodel_name='project.task')

    @api.onchange('account_analytic_id')
    def onchange_account_analytic_id(self):
        task_obj = self.env['project.task']
        for line in self:
            tasks = task_obj
            if line.account_analytic_id:
                tasks = line.account_analytic_id.catch_analytic_account_tasks()
                if not tasks and line.task_id:
                    line.task_id = task_obj
                if tasks and len(tasks) == 1:
                    line.task_id = tasks.id
            line.allowed_task_ids = [(6, 0, tasks.ids)]
