# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api
from pytz import timezone, utc


class HrHolidays(models.Model):
    _inherit = 'hr.holidays'

    @api.multi
    def onchange_employee(self, employee_id, date_to, date_from):
        res = super(HrHolidays, self).onchange_employee(employee_id)
        val = self.onchange_date_from(date_to, date_from, employee_id)
        if date_to and date_from:
            res['value']['number_of_days_temp'] = (
                val['value'].get('number_of_days_temp', False))
        return res

    @api.multi
    def onchange_date_from(self, date_to, date_from, employee_id):
        res = super(HrHolidays, self).onchange_date_from(date_to, date_from)
        if date_from and not date_to:
            date_to = res['value'].get('date_to', False)
        if (date_from and date_to and employee_id and
                res['value'].get('number_of_days_temp', False) > 0):
            res['value']['number_of_days_temp'] = self._remove_holidays(
                int(res['value'].get('number_of_days_temp')), date_to,
                date_from, employee_id)
        return res

    @api.multi
    def onchange_date_to(self, date_to, date_from, employee_id):
        res = super(HrHolidays, self).onchange_date_to(date_to, date_from)
        if (date_from and date_to and employee_id and
                res['value'].get('number_of_days_temp', False) > 0):
            res['value']['number_of_days_temp'] = self._remove_holidays(
                int(res['value'].get('number_of_days_temp')), date_to,
                date_from, employee_id)
        return res

    def _remove_holidays(self, days, date_to, date_from, employee_id):
        employee = self.env['hr.employee'].browse(employee_id)
        if not employee.address_home_id:
            return days
        date_to = fields.Date.to_string(
            fields.Datetime.from_string(date_to).date())
        date_from = fields.Date.to_string(
            fields.Datetime.from_string(date_from).date())
        cond = [('partner', '=', employee.address_home_id.id),
                ('date', '>=', date_from),
                ('date', '<=', date_to),
                ('festive', '=', True)]
        return days - len(self.env['res.partner.calendar.day'].search(cond))

    @api.multi
    def holidays_validate(self):
        res = super(HrHolidays, self).holidays_validate()
        for holiday in self.filtered(lambda x: x.type == 'remove'):
            days = holiday._find_calendar_days_from_holidays()
            days.write({'absence_type': holiday.holiday_status_id.id})
        return res

    @api.multi
    def holidays_refuse(self):
        res = super(HrHolidays, self).holidays_refuse()
        for holiday in self.filtered(lambda x: x.type == 'remove'):
            days = holiday._find_calendar_days_from_holidays()
            days.write({'absence_type': False})
        return res

    @api.multi
    def _find_calendar_days_from_holidays(self):
        calendar_day_obj = self.env['res.partner.calendar.day']
        new_date = (fields.Datetime.from_string(self.date_from) if
                    isinstance(self.date_from, str) else
                    self.date_from)
        new_date = new_date.replace(tzinfo=utc)
        date_from = new_date.astimezone(
            timezone(self.env.user.tz)).replace(tzinfo=None)
        new_date = (fields.Datetime.from_string(self.date_to) if
                    isinstance(self.date_to, str) else
                    self.date_to)
        new_date = new_date.replace(tzinfo=utc)
        date_to = new_date.astimezone(
            timezone(self.env.user.tz)).replace(tzinfo=None)
        cond = [('partner', '=', self.employee_id.address_home_id.id),
                ('date', '>=', date_from.date()),
                ('date', '<=', date_to.date())]
        days = calendar_day_obj.search(cond)
        return days
