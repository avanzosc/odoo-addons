# Copyright 2021 Berezi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class EventTrack(models.Model):
    _inherit = 'event.track'

    customer_id = fields.Many2one(
        string='Customer', comodel_name='res.partner',
        related='event_id.customer_id', store=True)
