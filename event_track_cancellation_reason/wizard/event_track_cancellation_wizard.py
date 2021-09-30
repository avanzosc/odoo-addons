# Copyright 2021 Berezi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class EventTrackCancellationWizard(models.TransientModel):
    _name = 'event.track.cancellation.wizard'
    _description = 'Wizard to cancel a Track'

    def default_get_event_track(self):
        return self.env['event.track'].browse(self.env.context.get('active_id'))

    def default_get_cancellation_reason(self):
        return self.env['event.track'].browse(self.env.context.get('active_id')).cancellation_reason_id

    def default_get_observation(self):
        return self.env['event.track'].browse(self.env.context.get('active_id')).observation

    def default_get_notification_date(self):
        return self.env['event.track'].browse(self.env.context.get('active_id')).notification_date

    def default_get_time_type(self):
        return self.env['event.track'].browse(self.env.context.get('active_id')).time_type_id

    event_track_id = fields.Many2one(
        string='Event Track', comodel_name='event.track', default=default_get_event_track)
    cancellation_reason_id = fields.Many2one(
        string='Cancellation Reason', comodel_name='cancellation.reason', default=default_get_cancellation_reason)
    observation = fields.Char(string='Cancellation Observations', default=default_get_observation)
    notification_date = fields.Datetime(string='Notification Date', default=default_get_notification_date)
    time_type_id = fields.Many2one(
        string='Time Type', comodel_name='project.time.type', default=default_get_time_type)

    def button_generate_cancellation(self):
        track = self.env['event.track'].browse(self.env.context.get('active_id'))
        stage = self.env.ref('website_event_track.event_track_stage5')
        track.write({
            'cancellation_reason_id': self.cancellation_reason_id,
            'observation': self.observation,
            'notification_date': self.notification_date,
            'time_type_id': self.time_type_id,
            'stage_id': stage.id,
            'is_cancel': True})
        if self.time_type_id.customer_billable or self.time_type_id.paid_employee:
            cond = [('date', '=', track.date.date()),
                    ('partner_id', '=', track.partner_id.id),
                    ('event_track_id', '=', track.id)]
            line = self.env['account.analytic.line'].search(cond, limit=1)
            if not line:
                track._create_analytic_line()
                if self.time_type_id.paid_employee:
                    analytic_line = self.env['account.analytic.line'].search(cond, limit=1)
                    if analytic_line:
                        analytic_line.non_allow_billable = True
