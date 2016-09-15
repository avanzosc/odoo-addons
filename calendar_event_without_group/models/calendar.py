# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, api, exceptions, _
from openerp import SUPERUSER_ID


class CalendarEvent(models.Model):
    _inherit = 'calendar.event'

    @api.multi
    def write(self, vals):
        if (self.env.uid != SUPERUSER_ID and
                self.filtered(lambda x: x.create_uid.id != self.env.uid)):
            raise exceptions.Warning(
                _("You can not change this meeting, because you are not the "
                  "user who created it"))
        return super(CalendarEvent, self).write(vals)


class CalendarAttendee(models.Model):
    _inherit = 'calendar.attendee'

    @api.multi
    def do_tentative(self, *args):
        self._user_control()
        return super(CalendarAttendee, self).do_tentative(*args)

    @api.multi
    def do_accept(self, *args):
        self._user_control()
        return super(CalendarAttendee, self).do_accept(*args)

    @api.multi
    def do_decline(self, *args):
        self._user_control()
        return super(CalendarAttendee, self).do_decline(*args)

    def _user_control(self):
        if (self.env.uid != SUPERUSER_ID and
                self.filtered(lambda x: x.event_id.create_uid.id !=
                              self.env.uid)):
            raise exceptions.Warning(
                _("You can not change this meeting, because you are not the "
                  "user who created it"))
