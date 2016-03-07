# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, exceptions, _


class WizEventAppendAssistant(models.TransientModel):
    _inherit = 'wiz.event.append.assistant'

    def _create_presence_from_wizard(self, track, event):
        presence = super(WizEventAppendAssistant,
                         self)._create_presence_from_wizard(track, event)
        presence.absence_type = track.absence_type
        self._update_partner_calendar_day(presence)
        return presence

    def _put_pending_presence_state(self, presence):
        res = super(WizEventAppendAssistant,
                    self)._put_pending_presence_state(presence)
        presence.absence_type = presence.track.absence_type
        self._update_partner_calendar_day(presence)
        return res

    def _update_partner_calendar_day(self, presence):
        calendar_day_obj = self.env['res.partner.calendar.day']
        cond = [('partner', '=', presence.partner.id),
                ('date', '=', presence.session_date_without_hour)]
        day = calendar_day_obj.search(cond, limit=1)
        if not day:
            raise exceptions.Warning(
                _('Calendar not found for employee %s')
                % presence.partner.name)
        day.absence_type = presence.absence_type
