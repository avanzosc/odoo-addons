# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api, exceptions, _


class CalendarHoliday(models.Model):
    _name = 'calendar.holiday'
    _description = 'Calendar holiday'

    name = fields.Char('Description', required=True)
    lines = fields.One2many(
        comodel_name='calendar.holiday.day',
        inverse_name='calendar_holiday', string='Calendar Holiday lines')


class CalendarHolidayDay(models.Model):
    _name = 'calendar.holiday.day'
    _description = 'Calendar holiday lines'
    _rec_name = 'date'
    _order = 'date'

    calendar_holiday = fields.Many2one(
        comodel_name='calendar.holiday', string='Calendar holiday',
        ondelete='cascade')
    date = fields.Date('Date')
    absence_type = fields.Many2one(
        'hr.holidays.status', string='Absence type')

    @api.model
    def create(self, vals):
        new_date = fields.Datetime.from_string(vals.get('date')).date()
        dates = self.search([])
        self._validate_unidate_date(dates, new_date)
        return super(CalendarHolidayDay, self).create(vals)

    @api.multi
    def write(self, vals):
        if vals.get('date', False):
            for line in self:
                new_date = fields.Datetime.from_string(vals.get('date')).date()
                cond = [('id', '!=', line.id)]
                dates = self.search(cond)
                line._validate_unidate_date(dates, new_date)
        return super(CalendarHolidayDay, self).write(vals)

    def _validate_unidate_date(self, dates, new_date):
        for line in dates:
            date = fields.Datetime.from_string(line.date).date()
            if date.month == new_date.month and date.day == new_date.day:
                raise exceptions.Warning(
                    _('There is already a date with day %s and month %s and'
                      ' year %s, in festive calendar %s') %
                    (str(date.day), str(date.month), str(date.year),
                     line.calendar_holiday.name))
