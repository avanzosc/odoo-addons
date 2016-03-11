# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, api, exceptions, _


class HrHolidays(models.Model):
    _inherit = 'hr.holidays'

    @api.multi
    def holidays_validate(self):
        res = super(HrHolidays, self).holidays_validate()
        for holiday in self:
            if holiday.employee_id.address_home_id:
                self._update_partner_calendar_day(
                    holiday, absence_type=holiday.holiday_status_id.id)
        return res

    @api.multi
    def holidays_refuse(self):
        for holiday in self:
            if (holiday.state == 'validate' and
                    holiday.employee_id.address_home_id):
                self._update_partner_calendar_day(holiday)
        res = super(HrHolidays, self).holidays_refuse()
        return res

    def _update_partner_calendar_day(self, holiday, absence_type=False):
        calendar_day_obj = self.env['res.partner.calendar.day']
        date_from = self._convert_date_to_local_format(
            holiday.date_from).strftime('%Y-%m-%d')
        date_to = self._convert_date_to_local_format(
            holiday.date_to).strftime('%Y-%m-%d')
        cond = [('partner', '=', holiday.employee_id.address_home_id.id),
                ('date', '>=', date_from),
                ('date', '<=', date_to)]
        days = calendar_day_obj.search(cond)
        if not days:
            raise exceptions.Warning(
                _('Calendar not found for employee %s')
                % holiday.employee_id.address_home_id.name)
        if absence_type:
            days.write({'absence': True,
                        'absence_type': absence_type})
            return True
        days.write({'absence': False,
                    'absence_type': False})
        presences = self._catch_employee_presences(holiday)
        for day in days:
            if day.absence_type_from_employee_contract:
                absence_type = day.absence_type_from_employee_contract
                day.write({'festive': True,
                           'absence_type': absence_type.id})
            else:
                for presence in presences:
                    session_date = presence.session_date_without_hour
                    if (session_date == day.date and
                            presence.session.absence_type):
                        day.write({'festive': True,
                                   'absence_type':
                                   presence.session.absence_type.id})
        return True
