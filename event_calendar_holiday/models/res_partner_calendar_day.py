# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields


class ResPartnerCalendarDay(models.Model):
    _inherit = 'res.partner.calendar.day'

    presences = fields.One2many(
        comodel_name='event.track.presence', string='Presences',
        inverse_name='partner_calendar_day')
