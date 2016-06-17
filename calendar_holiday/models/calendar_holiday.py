# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields


class CalendarHoliday(models.Model):
    _name = 'calendar.holiday'
    _description = 'Calendar holiday'

    name = fields.Char(string='Description', required=True)
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
    date = fields.Date(string='Date')
    absence_type = fields.Many2one(
        comodel_name='hr.holidays.status', string='Absence type')
