# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, _
from odoo.exceptions import UserError
import pytz


class EventEvent(models.Model):
    _inherit = 'event.event'

    replan_date_begin = fields.Date(
        string='Start Date', copy=False)
    replan_date_end = fields.Date(
        string='End Date', copy=False)
    replan_resource_calendar_id = fields.Many2one(
        string='Event Schedule', comodel_name='resource.calendar', copy=False)
    rescheduled_sessions = fields.Boolean(
        string='Rescheduled sessions', default=False, copy=False)

    def button_replan_sessions(self):
        if not self.replan_date_begin:
            raise UserError(_('You must enter the replanning start date.'))
        if not self.replan_date_end:
            raise UserError(_('You must enter the replanning end date.'))
        if not self.replan_resource_calendar_id:
            raise UserError(_('You must enter the replanning event schedule.'))
        sessions_for_unlink = self.env['event.track']
        sessions = self.track_ids.filtered(lambda x: not x.stage_id.is_done)
        if sessions:
            sessions = sessions.filtered(
                lambda x: not x.stage_id.is_cancel)
        for session in sessions:
            timezone = pytz.timezone(self.date_tz or 'UTC')
            session_date = session.date.replace(
                tzinfo=pytz.timezone('UTC')).astimezone(timezone)
            session_date = session_date.date()
            if (session_date >= self.replan_date_begin and
                    session_date <= self.replan_date_end):
                sessions_for_unlink += session
        if sessions_for_unlink:
            sessions_for_unlink.unlink()
        self.with_context(
            rep_date_begin=self.replan_date_begin,
            rep_date_end=self.replan_date_end,
            rep_calendar=self.replan_resource_calendar_id)._create_tracks()
        n = 1
        sessions = self.track_ids.sorted('date')
        for session in sessions:
            session.name = _('Session {}').format(n)
            n += 1
        self.rescheduled_sessions = True
