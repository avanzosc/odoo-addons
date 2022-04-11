# Copyright 2021 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api


class EventEvent(models.Model):
    _inherit = 'event.event'

    track_total_duration = fields.Float(
        string='Track Total Duration', readonly=True,
        compute='_track_total_duration')

    @api.depends('track_ids.duration')
    def _track_total_duration(self):
        for event in self:
            total_duration = 0.0
            for track in event.track_ids:
                total_duration += track.duration
            event.track_total_duration = total_duration
