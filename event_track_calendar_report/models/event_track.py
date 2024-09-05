# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class EventTrack(models.Model):
    _inherit = "event.track"

    name_for_calendar_report = fields.Char(
        string="Name for calendar report",
        compute="_compute_name_for_calendar_report",
        store=True,
        copy=False,
    )

    @api.depends("name", "event_id", "event_id.name")
    def _compute_name_for_calendar_report(self):
        for track in self:
            name = ""
            if track.event_id and track.event_id.name:
                name = track.event_id.name
            if track.name:
                name = "%s: %s" % (name, track.name)
            track.name_for_calendar_report = name
