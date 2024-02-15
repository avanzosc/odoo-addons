# Copyright 2021 Berezi - Iker - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class SlideChannel(models.Model):
    _inherit = "slide.channel"

    slide_ids = fields.One2many(copy=True)
    event_ids = fields.Many2many(
        string="Event",
        comodel_name="event.event",
        relation="rel_event_slides",
        column1="slides_id",
        column2="event_id",
    )
