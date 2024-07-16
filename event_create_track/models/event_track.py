# Copyright 2021 Berezi - Iker - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class EventTrack(models.Model):
    _inherit = "event.track"

    address_id = fields.Many2one(string="Location", comodel_name="res.partner")
    second_responsible_id = fields.Many2one(
        string="Assistant", comodel_name="res.partner"
    )

    def name_get(self):
        result = []
        for track in self:
            name = "{} {} {}".format(track.sudo().event_id.name, track.name, track.date)
            result.append((track.id, name))
        return result
