# Copyright 2021 Berezi - Iker - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class SlideChannel(models.Model):
    _inherit = 'slide.channel'

    event_ids = fields.Many2many(
        string='Event', comodel_name='event.event',
        relation='rel_event_slides', columm1='slides_ids', columm2='event_ids')
