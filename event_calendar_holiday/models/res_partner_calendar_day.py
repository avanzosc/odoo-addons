# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api


class ResPartnerCalendarDay(models.Model):
    _inherit = 'res.partner.calendar.day'

    @api.depends('presences', 'presences.state', 'presences.absence_type',
                 'presences.session_duration', 'presences.real_duration')
    def _calculate_estim_and_real_hours(self):
        for day in self:
            day.estimated_hours = 0.0
            day.real_hours = 0.0
            day.lit_estimated_hours = ('Estim: ' + str(day.estimated_hours))
            day.lit_real_hours = 'Real: ' + str(day.real_hours)
            for presence in day.presences:
                if not presence.absence_type:
                    if presence.state in('pending, completed'):
                        day.estimated_hours += presence.session_duration
                        day.lit_estimated_hours = ('Estim: ' +
                                                   str(day.estimated_hours))
                    if presence.state == 'completed':
                        day.real_hours += presence.real_duration
                        day.lit_real_hours = 'Real: ' + str(day.real_hours)

    presences = fields.One2many(
        comodel_name='event.track.presence', string='Presences',
        inverse_name='partner_calendar_day')
    estimated_hours = fields.Float(
        compute='_calculate_estim_and_real_hours', store=True)
    real_hours = fields.Float(
        compute='_calculate_estim_and_real_hours', store=True)
    lit_estimated_hours = fields.Char(
        string='Estimated hours literal', store=True,
        compute='_calculate_estim_and_real_hours')
    lit_real_hours = fields.Char(
        string='Real hours literal', store=True,
        compute='_calculate_estim_and_real_hours')
