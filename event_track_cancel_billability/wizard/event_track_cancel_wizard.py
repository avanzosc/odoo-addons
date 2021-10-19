# Copyright 2021 Berezi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, api


class EventTrackCancelWizard(models.TransientModel):
    _inherit = 'event.track.cancel.wizard'

    @api.onchange("notification_date")
    def onchange_non_billable(self):
        track = self.env['event.track'].browse(
            self.env.context.get('active_id'))
        if track.cancelled_company is True:
            self.time_type_id = self.env.ref(
                'event_track_cancel_reason.time_type4').id
        else:
            if track.notice_deadline and self.notification_date:
                if (track.notice_deadline > (self.notification_date)):
                    self.time_type_id = self.env.ref(
                        'event_track_cancel_reason.time_type3').id
                else:
                    self.time_type_id = self.env.ref(
                        'event_track_cancel_reason.time_type2').id
