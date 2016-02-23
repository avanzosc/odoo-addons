# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models, api


class WizEventAppendAssistant(models.TransientModel):
    _inherit = 'wiz.event.append.assistant'

    tasks = fields.Many2many('project.task', string='Add partner to the tasks')

    @api.model
    def default_get(self, var_fields):
        project_obj = self.env['project.project']
        task_obj = self.env['project.task']
        res = super(WizEventAppendAssistant, self).default_get(var_fields)
        cond = self._prepare_project_condition()
        projects = project_obj.search(cond)
        if projects:
            cond = [('project_id', 'in', projects.ids)]
            tasks = task_obj.search(cond)
            if tasks:
                res['tasks'] = [(6, 0, tasks.ids)]
        return res

    def _prepare_project_condition(self):
        event_obj = self.env['event.event']
        account_obj = self.env['account.analytic.account']
        accounts = self.env['account.analytic.account']
        event_ids = self.env.context.get('active_ids', False)
        events = event_obj.browse(event_ids)
        for event in events:
            if (event.project_id.analytic_account_id and
                    event.project_id.analytic_account_id not in accounts):
                accounts += event.project_id.analytic_account_id
        cond = [('parent_id', 'in', accounts.ids)]
        analytic_accounts = account_obj.search(cond)
        for account in analytic_accounts:
            if account not in accounts:
                accounts += account
        cond = [('analytic_account_id', 'in', accounts.ids)]
        return cond

    def _prepare_track_condition_search(self, event):
        cond = super(WizEventAppendAssistant,
                     self)._prepare_track_condition_search(event)
        if self.tasks:
            cond.append(('tasks', 'in', self.tasks.ids))
        return cond

    def _create_presence_from_wizard(self, track, event):
        result = super(WizEventAppendAssistant,
                       self)._create_presence_from_wizard(track, event)
        for task in track.tasks:
            if self.partner not in task.sessions_partners:
                task.sessions_partners = [(4, self.partner.id)]
        return result
