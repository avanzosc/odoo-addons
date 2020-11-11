# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, api


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    @api.model
    def create(self, vals):
        if ('account_id' in vals and vals.get('account_id', False) and
           ('project_id' not in vals or not vals.get('project_id', False))):
            cond = [('analytic_account_id', '=',  vals.get('account_id'))]
            project = self.env['project.project'].search(cond)
            if len(project) == 1:
                vals['project_id'] = project.id
        return super(AccountAnalyticLine, self).create(vals)

    @api.multi
    def write(self, vals):
        if ('account_id' in vals and vals.get('account_id', False) and
           ('project_id' not in vals or not vals.get('project_id', False))):
            cond = [('analytic_account_id', '=',  vals.get('account_id'))]
            project = self.env['project.project'].search(cond)
            if len(project) == 1:
                vals['project_id'] = project.id
        return super(AccountAnalyticLine, self).write(vals)
