# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api, exceptions, _
from dateutil.relativedelta import relativedelta
from datetime import datetime
from pytz import timezone, utc


class HrHolidays(models.Model):
    _inherit = 'hr.holidays'

    @api.multi
    def holidays_validate(self):
        calendar_day_obj = self.env['res.partner.calendar.day']
        res = super(HrHolidays, self).holidays_validate()
        for holiday in self:
            if holiday.employee_id.address_home_id:
                absence_type = holiday.holiday_status_id.id
                date_from, date_to, presences = self._catch_employee_presences(
                    holiday)
                if presences:
                    presences.update({'absence_type': absence_type})
                while date_from <= date_to:
                    cond = [('partner', '=',
                             holiday.employee_id.address_home_id.id),
                            ('date', '=', date_from)]
                    day = calendar_day_obj.search(cond, limit=1)
                    if not day:
                        raise exceptions.Warning(
                            _('Calendar not found for employee %s')
                            % holiday.employee_id.address_home_id.name)
                    day.absence_type = absence_type
                    date_from = (fields.Date.from_string(str(date_from)) +
                                 (relativedelta(days=1)))
                    date_from = datetime.strptime(
                        str(date_from), "%Y-%m-%d").date()
        return res

    @api.multi
    def holidays_refuse(self):
        calendar_day_obj = self.env['res.partner.calendar.day']
        for holiday in self:
            if (holiday.state == 'validate' and
                    holiday.employee_id.address_home_id):
                date_from, date_to, presences = self._catch_employee_presences(
                    holiday)
                for presence in presences:
                    presence.absence_type = presence.session.absence_type
                while date_from <= date_to:
                    cond = [('partner', '=',
                             holiday.employee_id.address_home_id.id),
                            ('date', '=', date_from)]
                    day = calendar_day_obj.search(cond, limit=1)
                    if not day:
                        raise exceptions.Warning(
                            _('Calendar not found for employee %s')
                            % holiday.employee_id.address_home_id.name)
                    day.absence_type = False
                    for presence in presences:
                        if presence.session_date_without_hour == day.date:
                            day.absence_type = presence.absence_type
                    date_from = (fields.Date.from_string(str(date_from)) +
                                 (relativedelta(days=1)))
                    date_from = datetime.strptime(
                        str(date_from), "%Y-%m-%d").date()
        res = super(HrHolidays, self).holidays_refuse()
        return res

    def _catch_employee_presences(self, holiday):
        presence_obj = self.env['event.track.presence']
        date_from = self._convert_date_to_local_format(
            holiday.date_from).strftime('%Y-%m-%d')
        date_from = datetime.strptime(str(date_from), "%Y-%m-%d").date()
        date_to = self._convert_date_to_local_format(
            holiday.date_to).strftime('%Y-%m-%d')
        date_to = datetime.strptime(str(date_to), "%Y-%m-%d").date()
        cond = [('partner', '=',
                 holiday.employee_id.address_home_id.id),
                ('session_date_without_hour', '>=', date_from),
                ('session_date_without_hour', '<=', date_to)]
        presences = presence_obj.search(cond)
        return date_from, date_to, presences

    def _convert_date_to_local_format(self, date):
        new_date = fields.Datetime.from_string(date).date()
        local_date = datetime(
            int(new_date.strftime("%Y")), int(new_date.strftime("%m")),
            int(new_date.strftime("%d")), int(date[11:13]), int(date[14:16]),
            int(date[17:19]), tzinfo=utc).astimezone(
            timezone(self.env.user.tz)).replace(tzinfo=None)
        return local_date
