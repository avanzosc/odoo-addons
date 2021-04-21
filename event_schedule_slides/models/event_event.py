# Copyright 2021 Berezi - Iker - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class EventEvent(models.Model):
    _inherit = 'event.event'

    slides_ids = fields.Many2many(
        string='Courses', comodel_name='slide.channel',
        relation='rel_event_slides', columm1='event_ids', columm2='slides_ids')
