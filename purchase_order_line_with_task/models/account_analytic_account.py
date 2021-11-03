# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    def catch_analytic_account_tasks(self):
        allowed_tasks = self.env['project.task']
        cond = [('analytic_account_id', '=', self.id)]
        project = self.env['project.project'].search(cond, limit=1)
        if project:
            allowed_tasks = project.task_ids
        return allowed_tasks
