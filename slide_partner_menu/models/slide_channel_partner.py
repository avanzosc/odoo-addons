# Copyright 2021 Berezi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class SlideChannelPartner(models.Model):
    _inherit = 'slide.channel.partner'

    event_id = fields.Many2one(
        string='Event', comodel_name='event.event',
        related='event_registration_id.event_id', store=True)
