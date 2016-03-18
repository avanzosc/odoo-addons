# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api, exceptions, _
from dateutil.relativedelta import relativedelta
from datetime import datetime
from pytz import timezone, utc


class EventEvent(models.Model):
    _inherit = 'event.event'

    @api.depends('date_begin')
    def _calculate_date_begin_without_hour(self):
        for event in self:
            event.date_begin_without_hour = self._convert_date_to_local_format(
                event.date_begin)

    @api.depends('date_end')
    def _calculate_date_end_without_hour(self):
        for event in self:
            event.date_end_without_hour = self._convert_date_to_local_format(
                event.date_end)

    date_begin_without_hour = fields.Date(
        'Date begin without hour', store=True,
        compute='_calculate_date_begin_without_hour')
    date_end_without_hour = fields.Date(
        'Date end without hour', store=True,
        compute='_calculate_date_end_without_hour')

    def _convert_date_to_local_format(self, date):
        if not date:
            return False
        new_date = fields.Datetime.from_string(date).date()
        local_date = datetime(
            int(new_date.strftime("%Y")), int(new_date.strftime("%m")),
            int(new_date.strftime("%d")), int(date[11:13]), int(date[14:16]),
            int(date[17:19]), tzinfo=utc).astimezone(
            timezone(self.env.user.tz)).replace(tzinfo=None)
        local_date.date()
        return local_date


class EventRegistration(models.Model):
    _inherit = 'event.registration'

    @api.depends('partner_id', 'event_id.date_begin', 'event_id.date_end')
    def _search_contracts_permitted(self):
        contract_obj = self.env['hr.contract']
        for reg in self:
            if (reg.partner_id and reg.event_id.date_begin and
                    reg.event_id.date_end):
                date_start = reg._convert_date_to_local_format(
                    reg.event_id.date_begin).date().strftime('%Y-%m-%d')
                date_end = reg._convert_date_to_local_format(
                    reg.event_id.date_end).date().strftime('%Y-%m-%d')
                cond = [('partner', '=', reg.partner_id.id),
                        ('date_start', '<=', date_start), '|',
                        ('date_end', '=', False),
                        ('date_end', '>=', date_end)]
                contracts = contract_obj.search(cond)
                reg.contracts_permitted = [(6, 0, contracts.ids)]
                if len(contracts) == 1:
                    reg.contract = contracts[0].id

    contract = fields.Many2one('hr.contract', string='Employee contract')
    address_home_id = fields.Many2one(
        'res.partner', related='partner_id.employee.address_home_id',
        string='Employee', store=True)
    contracts_permitted = fields.Many2many(
        'hr.contract', string='Contracts permitted',
        compute='_search_contracts_permitted')

    @api.multi
    def registration_open(self):
        self.ensure_one()
        wiz_obj = self.env['wiz.event.append.assistant']
        if self.address_home_id and not self.contract:
            raise exceptions.Warning(
                _("You must enter the employee's contract"))
        result = super(EventRegistration, self).registration_open()
        wiz = wiz_obj.browse(result['res_id'])
        if self.contract:
            wiz.write({'contract': self.contract.id})
        return result

    def _convert_date_to_local_format(self, date):
        if not date:
            return False
        new_date = fields.Datetime.from_string(date).date()
        local_date = datetime(
            int(new_date.strftime("%Y")), int(new_date.strftime("%m")),
            int(new_date.strftime("%d")), int(date[11:13]), int(date[14:16]),
            int(date[17:19]), tzinfo=utc).astimezone(
            timezone(self.env.user.tz)).replace(tzinfo=None)
        local_date.date()
        return local_date


class EventTrackPresence(models.Model):
    _inherit = 'event.track.presence'

    def _update_employee_days(self, cancel_presence=False):
        calendar_day_obj = self.env['res.partner.calendar.day']
        holidays_obj = self.env['hr.holidays']
        cond = [('partner', '=', self.partner.id),
                ('date', '=', self.session_date_without_hour)]
        day = calendar_day_obj.search(cond, limit=1)
        if not day:
            raise exceptions.Warning(
                _('Calendar not found for employee %s')
                % self.partner.name)
        if self.absence_type:
            day.write({'festive': True,
                       'absence_type': self.absence_type.id})
        if cancel_presence:
            day.write({'festive': False,
                       'absence_type': False})
            if day.absence_type_from_employee_contract:
                absence_type = day.absence_type_from_employee_contract
                day.write({'festive': True,
                           'absence_type': absence_type.id})
        presence_date = self._put_utc_format_date(
            self.session_date_without_hour, 0.0).strftime(
            '%Y-%m-%d %H:%M:%S')
        cond = [('employee_id', '=', self.partner.id),
                ('date_from', '>=', presence_date),
                ('date_to', '<=', presence_date),
                ('type', '=', 'remove'),
                ('state', '=', 'validate')]
        holiday = holidays_obj.search(cond, limit=1)
        if holiday:
            day.write({'absence': True,
                       'absence_type': holiday.holiday_status_id.id})

    def _put_utc_format_date(self, date, time):
        new_date = (datetime.strptime(str(date), '%Y-%m-%d') +
                    relativedelta(hours=float(time)))
        local = timezone(self.env.user.tz)
        local_dt = local.localize(new_date, is_dst=None)
        utc_dt = local_dt.astimezone(utc)
        return utc_dt
