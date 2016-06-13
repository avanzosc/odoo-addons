# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models, api, _
from dateutil.relativedelta import relativedelta


class WizEventAppendAssistant(models.TransientModel):
    _inherit = 'wiz.event.append.assistant'

    permitted_tasks = fields.Many2many('project.task', string='Permited tasks')
    tasks = fields.Many2many('project.task', string='Add partner to the tasks')

    @api.model
    def default_get(self, var_fields):
        res = super(WizEventAppendAssistant, self).default_get(var_fields)
        if res or (self.from_date and self.to_date):
            res = self._find_task_for_append_assistant(res)
        return res

    @api.multi
    @api.onchange('from_date', 'to_date', 'partner')
    def onchange_dates_and_partner(self):
        self.ensure_one()
        res = super(WizEventAppendAssistant, self).onchange_dates_and_partner()
        if not res:
            res = self._find_task_for_append_assistant(res)
        if not res:
            if not self.tasks:
                return {'warning': {
                        'title': _('Error in dates'),
                        'message':
                        _('Not tasks found for introduced dates')}}
        return res

    def _find_task_for_append_assistant(self, res):
        tasks = self._prepare_tasks_search_condition(res)
        if not tasks:
            if res:
                res.update({'permitted_tasks': [(6, 0, [])],
                            'tasks': [(6, 0, [])]})
            else:
                self.update({'permitted_tasks': [(6, 0, [])],
                             'tasks': [(6, 0, [])]})
        else:
            if res:
                res.update({'permitted_tasks': [(6, 0, tasks.ids)],
                            'tasks': [(6, 0, tasks.ids)]})
            else:
                self.update({'permitted_tasks': [(6, 0, tasks.ids)],
                             'tasks': [(6, 0, tasks.ids)]})
        return res

    def _prepare_tasks_search_condition(self, res):
        session_obj = self.env['event.track']
        event_obj = self.env['event.event']
        tasks = self.env['project.task']
        if (res.get('from_date', self.from_date) and res.get('to_date',
                                                             self.to_date)):
            from_date = event_obj._convert_date_to_local_format(
                res.get('from_date', self.from_date)).date()
            from_date = event_obj._put_utc_format_date(
                from_date, 0.0).strftime('%Y-%m-%d %H:%M:%S')
            to_date = event_obj._convert_date_to_local_format(
                res.get('to_date', self.to_date)).date()
            to_date = event_obj._put_utc_format_date(
                to_date, 0.0).strftime('%Y-%m-%d %H:%M:%S')
            cond = [('event_id', 'in', self.env.context.get('active_ids')),
                    ('date', '>=', from_date),
                    ('date', '<=', to_date),
                    ('date', '!=', False)]
            sessions = session_obj.search(cond)
            for session in sessions:
                for task in session.tasks:
                    if task not in tasks:
                        tasks += task
        return tasks

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
        event_obj = self.env['event.event']
        if event.sale_order.project_by_task == 'yes':
            from_date, to_date = self._calc_dates_for_search_track(
                self.from_date, self.to_date)
            fbegin = event_obj._convert_date_to_local_format_with_hour(
                event.date_begin).strftime('%Y-%m-%d %H:%M:%S')
            fbegin = fields.Datetime.from_string(fbegin)
            if (fbegin.strftime('%H') != '00' or
                    fbegin.strftime('%M') != '00' or
                    fbegin.strftime('%S') != '00'):
                to_date = (fields.Datetime.from_string(str(to_date)) +
                           (relativedelta(days=1)))
                to_date = fields.Datetime.to_string(to_date)
            cond = [('id', 'in', event.track_ids.ids),
                    ('date', '!=', False),
                    ('date', '>=', from_date),
                    ('date', '<=', to_date)]
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
