# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, _
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError


class CalendarEvent(models.Model):
    _inherit = 'calendar.event'

    timesheet_line_ids = fields.One2many(
        string='Timesheet', comodel_name='account.analytic.line',
        inverse_name='meeting_id')
    state = fields.Selection(
        [
            ("created", "Created"),
            ("scheduled", "Scheduled"),
            ("done", "Done"),
            ("canceled", "Cancelled"),
        ],
        string="Status",
        tracking=3,
        default="created")

    def _catch_values_for_create_timesheet_line(self):
        timesheet_line_vals = {
            'name': self.name,
            'user_id': self.user_id.id,
            'meeting_id': self.id,
            'company_id': self.user_id.company_id.id}
        if self.task_id:
            timesheet_line_vals['id'] = self.task_id.id
            if self.user_id:
                cond = [('user_id', '=', self.user_id.id)]
                employee = self.env['hr.employee'].search(cond, limit=1)
                if not employee:
                    raise UserError(
                        _('Employee not found for user: {}').format(
                            self.user_id.name))
                if self.allday is True:
                    day = self.start_date.weekday()
                    lines = (
                        employee.resource_calendar_id.attendance_ids.filtered(
                            lambda x: x.dayofweek == str(day)))
                    duration = sum(lines.mapped('hour_gap'))
                    self.duration = duration
                    self.start = self.start_date
                timesheet_line_vals.update({
                    'date': self.start,
                    'unit_amount': self.duration,
                    'task_id': self.task_id.id,
                    'project_id': self.task_id.project_id.id,
                    'account_id': (
                        self.task_id.project_id.analytic_account_id.id),
                    'employee_id': employee.id})
        else:
            raise ValidationError(
                _("You must introduce a task for the meeting."))
        return timesheet_line_vals

    def _create_timesheet_line(self):
        values = self._catch_values_for_create_timesheet_line()
        self.env['account.analytic.line'].create(values)

    def write(self, vals):
        res = super(CalendarEvent, self).write(vals)
        if vals.get('state') == 'done':
            for meeting in self:
                cond = [('date', '=', meeting.start_date),
                        ('user_id', '=', meeting.user_id.id),
                        ('meeting_id', '=', meeting.id)]
                line = self.env['account.analytic.line'].search(
                    cond, limit=1)
                if not line:
                    meeting._create_timesheet_line()
        return res
