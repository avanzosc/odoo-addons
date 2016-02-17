# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api, _
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pytz


class ProjectProject(models.Model):
    _inherit = 'project.project'

    @api.multi
    def write(self, vals):
        if (self.env.context.get('sale_order_create_event', False) and
                vals.get('date', False)):
            vals.pop('date')
        return super(ProjectProject, self).write(vals)


class ProjectTask(models.Model):
    _inherit = 'project.task'

    @api.multi
    def _calc_num_sessions(self):
        for task in self:
            task.num_sessions = len(task.sessions)

    sessions = fields.Many2many(
        comodel_name="event.track", relation="task_session_project_relation",
        column1="task_id", column2="track_id", copy=False, string="Sessions")
    num_sessions = fields.Integer(
        string='# Session', compute='_calc_num_sessions')
    recurring_service = fields.Boolean(
        'Recurring Service',
        related='service_project_sale_line.recurring_service')
    january = fields.Boolean(
        'January', related='service_project_sale_line.january')
    february = fields.Boolean(
        'February', related='service_project_sale_line.february')
    march = fields.Boolean(
        'March', related='service_project_sale_line.march')
    april = fields.Boolean(
        'April', related='service_project_sale_line.april')
    may = fields.Boolean(
        'May', related='service_project_sale_line.may')
    june = fields.Boolean(
        'June', related='service_project_sale_line.june')
    july = fields.Boolean(
        'July', related='service_project_sale_line.july')
    august = fields.Boolean(
        'August', related='service_project_sale_line.august')
    september = fields.Boolean(
        'September', related='service_project_sale_line.september')
    october = fields.Boolean(
        'October', related='service_project_sale_line.october')
    november = fields.Boolean(
        'November', related='service_project_sale_line.november')
    december = fields.Boolean(
        'December', related='service_project_sale_line.december')
    week1 = fields.Boolean(
        'Week 1', related='service_project_sale_line.week1')
    week2 = fields.Boolean(
        'Week 2', related='service_project_sale_line.week2')
    week3 = fields.Boolean(
        'Week 3', related='service_project_sale_line.week3')
    week4 = fields.Boolean(
        'Week 4', related='service_project_sale_line.week4')
    week5 = fields.Boolean(
        'Week 5', related='service_project_sale_line.week5')
    monday = fields.Boolean(
        'Monday', related='service_project_sale_line.monday')
    tuesday = fields.Boolean(
        'Tuesday', related='service_project_sale_line.tuesday')
    wednesday = fields.Boolean(
        'Wednesday', related='service_project_sale_line.wednesday')
    thursday = fields.Boolean(
        'Thursday', related='service_project_sale_line.thursday')
    friday = fields.Boolean(
        'Friday', related='service_project_sale_line.friday')
    saturday = fields.Boolean(
        'Saturday', related='service_project_sale_line.saturday')
    sunday = fields.Boolean(
        'Sunday', related='service_project_sale_line.sunday')

    def _create_task_from_procurement_service_project(self, procurement):
        task = super(
            ProjectTask,
            self)._create_task_from_procurement_service_project(procurement)
        if task.service_project_sale_line.order_id.project_by_task == 'yes':
            parent_account = task.project_id.analytic_account_id
            code = self.env['ir.sequence'].get('account.analytic.account')
            vals = {'name': (task.project_id.name + ': ' +
                             task.service_project_sale_line.product_id.name),
                    'use_tasks': True,
                    'type': 'contract',
                    'date_start':
                    task.project_id.analytic_account_id.date_start,
                    'date': task.project_id.analytic_account_id.date_start,
                    'parent_id': parent_account.id,
                    'code': code,
                    'partner_id':
                    task.project_id.analytic_account_id.partner_id.id}
            new_account = self.env['account.analytic.account'].create(vals)
            cond = [('analytic_account_id', '=', new_account.id)]
            project = self.env['project.project'].search(cond, limit=1)
            task.project_id = project.id
            new_account.date = parent_account.date
            project.date = parent_account.date
        return task

    @api.multi
    def show_sessions_from_task(self):
        self.ensure_one()
        return {'name': _('Sessions'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree, form',
                'res_model': 'event.track',
                'domain': [('id', 'in', self.sessions.ids)]}

    @api.multi
    def button_recalculate_sessions(self):
        self.ensure_one()
        self.sessions.unlink()
        num_session = 0
        fec_ini = fields.Datetime.from_string(self.date_start).date()
        if fec_ini.day != 1:
            while fec_ini.day != 1:
                fec_ini = fec_ini + relativedelta(days=-1)
        if fec_ini.weekday() == 0:
            num_week = 0
        else:
            num_week = 1
        month = fec_ini.month
        while fec_ini <= fields.Datetime.from_string(self.date_end).date():
            if month != fec_ini.month:
                month = fec_ini.month
                if fec_ini.weekday() == 0:
                    num_week = 0
                else:
                    num_week = 1
            if fec_ini.weekday() == 0:
                num_week += 1
            if fec_ini >= fields.Datetime.from_string(self.date_start).date():
                valid = self._validate_event_session_month(self, fec_ini)
                if valid:
                    valid = self._validate_event_session_week(
                        self, num_week)
                if valid:
                    valid = self._validate_event_session_day(self, fec_ini)
                if valid:
                    num_session += 1
                    self._create_session_from_task(
                        self.event_id, num_session, fec_ini)
            fec_ini = fec_ini + relativedelta(days=+1)

    def _validate_event_session_month(self, line, fec_ini):
        valid = False
        month = fec_ini.month
        if ((line.january and month == 1) or
            (line.february and month == 2) or
            (line.march and month == 3) or
            (line.april and month == 4) or
            (line.may and month == 5) or
            (line.june and month == 6) or
            (line.july and month == 7) or
            (line.august and month == 8) or
            (line.september and month == 9) or
            (line.october and month == 10) or
            (line.november and month == 11) or
                (line.december and month == 12)):
            valid = True
        return valid

    def _validate_event_session_week(self, line, num_week):
        valid = False
        if ((line.week1 and num_week == 1) or
            (line.week2 and num_week == 2) or
            (line.week3 and num_week == 3) or
            (line.week4 and num_week == 4) or
                (line.week5 and num_week == 5)):
            valid = True
        return valid

    def _validate_event_session_day(self, line, fec_ini):
        valid = False
        day = fec_ini.weekday()
        if ((line.monday and day == 0) or
            (line.tuesday and day == 1) or
            (line.wednesday and day == 2) or
            (line.thursday and day == 3) or
            (line.friday and day == 4) or
            (line.saturday and day == 5) or
                (line.sunday and day == 6)):
            valid = True
        return valid

    def _create_session_from_task(self, event, num_session, date):
        vals = self._prepare_session_data_from_task(event, num_session, date)
        self.env['event.track'].create(vals)
        duration = sum(self.mapped('sessions.duration'))
        self.planned_hours = duration

    def _prepare_session_data_from_task(self, event, num_session, date):
        new_date = (datetime.strptime(str(date), '%Y-%m-%d') +
                    relativedelta(hours=float(0.0)))
        local = pytz.timezone(self.env.user.tz)
        local_dt = local.localize(new_date, is_dst=None)
        utc_dt = local_dt.astimezone(pytz.utc)
        duration = (self.service_project_sale_line.product_uom_qty *
                    (self.service_project_sale_line.performance or 1))
        vals = {'name': (_('Session %s for %s') %
                         (str(num_session),
                          self.service_project_sale_line.product_id.name)),
                'event_id': event.id,
                'date': utc_dt,
                'duration': duration,
                'tasks': [(4, self.id)]}
        return vals
