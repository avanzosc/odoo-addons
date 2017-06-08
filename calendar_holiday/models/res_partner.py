# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api, exceptions, _
from dateutil.relativedelta import relativedelta


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def _generate_calendar(self, year):
        calendar_obj = self.env['res.partner.calendar']
        day_vals = []
        start_date = fields.Date.from_string('{}-01-01'.format(year))
        end_date = fields.Date.from_string('{}-12-31'.format(year))
        while start_date <= end_date:
            day_vals.append((0, 0, {'partner': self.id, 'date': start_date}))
            start_date = (fields.Date.from_string(str(start_date)) +
                          (relativedelta(days=1)))
        cond = [('partner', '=', self.id),
                ('year', '=', year)]
        calendar = calendar_obj.search(cond, limit=1)
        if calendar:
            calendar.dates.unlink()
            calendar.write({'dates': day_vals})
        else:
            calendar_vals = {
                'partner': self.id,
                'year': year,
                'dates': day_vals,
            }
            calendar = calendar_obj.create(calendar_vals)

    def _put_estimated_hours_in_calendar(self, year, contract):
        partner_calendar_day_obj = self.env['res.partner.calendar.day']
        for attendance in contract.working_hours.attendance_ids:
            cond = [('partner', '=', contract.partner.id),
                    ('year', '=', year),
                    ('weekday', '=', attendance.dayofweek)]
            if attendance.date_from:
                cond.append(('date', '>=', attendance.date_from))
            elif contract.date_start:
                cond.append(('date', '>=', contract.date_start))
            if contract.date_end:
                cond.append(('date', '<=', contract.date_end))
            else:
                cond.append(('date', '<=', "{}-12-31".format(year)))
            partner_calendar_days = partner_calendar_day_obj.search(cond)
            if partner_calendar_days:
                for day in partner_calendar_days:
                    hours = attendance.hour_to - attendance.hour_from
                    day.estimated_hours = day.estimated_hours + hours

    def _generate_festives_in_calendar(self, year, calendar):
        calendar_obj = self.env['res.partner.calendar']
        calendar_day_obj = self.env['res.partner.calendar.day']
        for line in calendar.lines:
            date = fields.Datetime.from_string(line.date).date()
            new_date = str(year) + '-' + str(date.month) + '-' + str(date.day)
            cond = [('partner', '=', self.id),
                    ('year', '=', year)]
            partner_calendar = calendar_obj.search(cond, limit=1)
            if not partner_calendar:
                raise exceptions.Warning(
                    _('The calendar %s was not found, for employee %s')
                    % (str(year), self.name))
            cond = [('partner', '=', self.id),
                    ('date', '=', new_date)]
            calendar_day = calendar_day_obj.search(cond, limit=1)
            if not calendar_day:
                raise exceptions.Warning(
                    _('The day %s was not found in the calendar %s, for'
                      ' employee %s') % (new_date, str(year), self.name))
            calendar_day.write({'estimated_hours': 0,
                                'festive': True,
                                'absence_type': line.absence_type.id,
                                'calendar_holiday_day': line.id,
                                'absence_type_from_employee_contract':
                                line.absence_type.id})


class ResPartnerCalendar(models.Model):
    _name = 'res.partner.calendar'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _description = 'Employee calendar'
    _rec_name = 'year'

    partner = fields.Many2one(
        comodel_name='res.partner', string='Partner', ondelete='cascade')
    year = fields.Integer(string='Year', size=4)
    dates = fields.One2many(
        comodel_name='res.partner.calendar.day', inverse_name='calendar',
        string='Calendar dates')

    @api.model
    def create(self, values):
        res = super(ResPartnerCalendar, self).create(values)
        if values.get('partner', False):
            res.message_subscribe([values.get('partner')])
        return res

    @api.multi
    def write(self, values):
        res = super(ResPartnerCalendar, self).write(values)
        if values.get('partner', False):
            self.message_subscribe([values.get('partner')])
        return res


class ResPartnerCalendarDay(models.Model):
    _name = 'res.partner.calendar.day'
    _description = 'Employee calendar day'
    _rec_name = 'date'

    @api.depends('date')
    def _compute_weekday(self):
        for day in self:
            date = fields.Date.from_string(day.date)
            day.year = date.year
            day.weekday = str(date.weekday())

    calendar = fields.Many2one(
        comodel_name='res.partner.calendar', string='Calendar',
        ondelete='cascade')
    partner = fields.Many2one(
        comodel_name='res.partner', related='calendar.partner',
        string='Partner', store=True, select=True)
    date = fields.Date(string='Date', select=True)
    year = fields.Integer(
        string='year', compute='_compute_weekday', store=True)
    weekday = fields.Selection(
        [('0', 'Monday'),
         ('1', 'Tuesday'),
         ('2', 'Wednesday'),
         ('3', 'Thursday'),
         ('4', 'Friday'),
         ('5', 'Saturday'),
         ('6', 'Sunday')],
        string='Weekday', compute='_compute_weekday', store=True)
    contract = fields.Many2one(
        comodel_name='hr.contract', string='Partner contract')
    estimated_hours = fields.Float(string='Estimated hours', default=0.0)
    real_hours = fields.Float(string='Real hours', default=0.0)
    festive = fields.Boolean(string='Festive', default=False)
    absence_type = fields.Many2one(
        comodel_name='hr.holidays.status', string='Absence type')
    absence_type_from_employee_contract = fields.Many2one(
        comodel_name='hr.holidays.status', string='Absence type')
    calendar_holiday_day = fields.Many2one(
        comodel_name='calendar.holiday.day', string='Calendar holiday day')
