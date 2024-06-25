# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class EventRegistration(models.Model):
    _inherit = "event.registration"

    headquarter_id = fields.Many2one(
        string="Headquarter",
        comodel_name="res.partner",
        related="event_id.organizer_id",
        store=True,
        copy=False,
    )
