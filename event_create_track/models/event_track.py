# Copyright 2021 Berezi - Iker - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class EventTrack(models.Model):
    _inherit = 'event.track'

    def name_get(self):
        result = []
        for track in self:
            name = u'{} {} {}'.format(
                track.event_id.name, track.name, track.date)
            result.append((track.id, name))
        return result
