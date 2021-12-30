# Copyright 2021 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields


class EventTrack(models.Model):
    _inherit = "event.track"

    resource_id = fields.Many2one(
        string="Resource", comodel_name="resource.resource", store=True,
        related="event_id.resource_id")