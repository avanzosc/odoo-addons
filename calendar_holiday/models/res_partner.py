# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, exceptions, _
from dateutil.relativedelta import relativedelta
from datetime import datetime


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def _generate_calendar(self, year):
        calendar_obj = self.env['res.partner.calendar']
        calendar_day_obj = self.env['res.partner.calendar.day']
        follower_obj = self.env['mail.followers']
        cond = [('partner', '=', self.id),
                ('year', '=', year)]
        calendar = calendar_obj.search(cond, limit=1)
        if calendar:
            calendar.dates.unlink()
        else:
            calendar_vals = {'partner': self.id,
                             'year': year}
            calendar = calendar_obj.create(calendar_vals)
            follower_obj.create({'res_model': 'res.partner.calendar',
                                 'res_id': calendar.id,
                                 'partner_id': self.id})
        start_date = datetime.strptime(str(year) + '-01-01', '%Y-%m-%d').date()
        end_date = datetime.strptime(str(year) + '-12-31', '%Y-%m-%d').date()
        while start_date.year == end_date.year:
            day_vals = {'calendar': calendar.id,
                        'partner': self.id,
                        'date': start_date}
            calendar_day_obj.create(day_vals)
            start_date = (fields.Date.from_string(str(start_date)) +
                          (relativedelta(days=1)))

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
            cond = [('calendar', '=', partner_calendar.id),
                    ('partner', '=', self.id),
                    ('date', '=', new_date)]
            calendar_day = calendar_day_obj.search(cond, limit=1)
            if not calendar_day:
                raise exceptions.Warning(
                    _('The day %s was not found in the calendar %s, for'
                      ' employee %s') % (new_date, str(year), self.name))
            calendar_day.write({'festive': True,
                                'absence_type': line.absence_type.id,
                                'absence_type_from_employee_contract':
                                line.absence_type.id})


class ResPartnerCalendar(models.Model):
    _name = 'res.partner.calendar'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _description = 'Partner calendar'
    _rec_name = 'year'

    partner = fields.Many2one(
        comodel_name='res.partner', string='Partner', ondelete='cascade')
    year = fields.Integer('Year', size=4)
    dates = fields.One2many(
        comodel_name='res.partner.calendar.day', inverse_name='calendar',
        string='Calendar dates')


class ResPartnerCalendarDay(models.Model):
    _name = 'res.partner.calendar.day'
    _description = 'Partner calendar day'
    _rec_name = 'date'

    calendar = fields.Many2one(
        comodel_name='res.partner.calendar', string='Partner calendar',
        ondelete='cascade')
    partner = fields.Many2one(
        'res.partner', related='calendar.partner', string='Partner',
        store=True)
    date = fields.Date('Date')
    contract = fields.Many2one(
        comodel_name='hr.contract', string='Partner contract')
    estimated_hours = fields.Float('Estimated hours', default=0.0)
    real_hours = fields.Float('Real hours', default=0.0)
    festive = fields.Boolean('Festive', default=False)
    absence_type = fields.Many2one(
        'hr.holidays.status', string='Absence type')
    absence_type_from_employee_contract = fields.Many2one(
        'hr.holidays.status', string='Absence type')
