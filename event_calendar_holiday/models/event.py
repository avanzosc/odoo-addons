# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api


class EventEvent(models.Model):
    _inherit = 'event.event'

    def _put_festives_in_sesions_from_sale_contract(self, calendars):
        for track in self.track_ids:
            for calendar in calendars:
                for day in calendar.lines:
                    track_month = fields.Datetime.from_string(
                        track.session_date).date().month
                    day_month = fields.Datetime.from_string(
                        day.date).date().month
                    track_day = fields.Datetime.from_string(
                        track.session_date).date().day
                    day_day = fields.Datetime.from_string(
                        day.date).date().day
                    if track_month == day_month and track_day == day_day:
                        track.absence_type = day.absence_type


class EventTrack(models.Model):
    _inherit = 'event.track'

    absence_type = fields.Many2one(
        'hr.holidays.status', string='Absence type')


class EventTrackPresence(models.Model):
    _inherit = 'event.track.presence'

    @api.depends('session_date_without_hour')
    def _calculate_partner_calendar_day(self):
        day_obj = self.env['res.partner.calendar.day']
        for presence in self:
            presence.partner_calendar_day = False
            if presence.session_date_without_hour:
                cond = [('partner', '=', presence.partner.id),
                        ('date', '=', presence.session_date_without_hour)]
                day = day_obj.search(cond)
                if day:
                    presence.partner_calendar_day = day.id

    partner_calendar_day = fields.Many2one(
        'res.partner.calendar.day', string='Employee calendar day',
        compute='_calculate_partner_calendar_day', store=True)
    absence_type = fields.Many2one(
        'hr.holidays.status', string='Absence type')
