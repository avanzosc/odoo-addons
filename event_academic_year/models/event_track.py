# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class EventTrack(models.Model):
    _inherit = "event.track"

    academic_year_id = fields.Many2one(
        string="Academic year",
        comodel_name="event.academic.year",
        related="event_id.academic_year_id",
        store=True,
        copy=False,
    )
