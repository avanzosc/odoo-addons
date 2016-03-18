# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api
from datetime import datetime
from pytz import timezone, utc


class HrHolidays(models.Model):
    _inherit = 'hr.holidays'

    @api.multi
    def holidays_validate(self):
        res = super(HrHolidays, self).holidays_validate()
        for holiday in self:
            if holiday.employee_id.address_home_id:
                absence_type = holiday.holiday_status_id.id
                presences = self._catch_employee_presences(holiday)
                if presences:
                    presences.write({'absence_type': absence_type})
        return res

    @api.multi
    def holidays_refuse(self):
        for holiday in self:
            if (holiday.state == 'validate' and
                    holiday.employee_id.address_home_id):
                presences = self._catch_employee_presences(holiday)
                for presence in presences:
                    presence.absence_type = presence.session.absence_type
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
        return presences

    def _convert_date_to_local_format(self, date):
        new_date = fields.Datetime.from_string(date).date()
        local_date = datetime(
            int(new_date.strftime("%Y")), int(new_date.strftime("%m")),
            int(new_date.strftime("%d")), int(date[11:13]), int(date[14:16]),
            int(date[17:19]), tzinfo=utc).astimezone(
            timezone(self.env.user.tz)).replace(tzinfo=None)
        return local_date
