# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class CrmClaim(models.Model):
    _inherit = "crm.claim"

    event_id = fields.Many2one(string="Event", comodel_name="event.event")
    event_track_id = fields.Many2one(string="Event track", comodel_name="event.track")
    event_responsible_id = fields.Many2one(
        string="Event responsible", related="event_id.user_id", store=True
    )
