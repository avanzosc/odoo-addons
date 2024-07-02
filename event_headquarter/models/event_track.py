# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class EventTrack(models.Model):
    _inherit = "event.track"

    headquarter_id = fields.Many2one(
        string="Headquarter",
        comodel_name="res.partner",
        related="event_id.organizer_id",
        store=True,
    )

    def _catch_values_for_create_analytic_line(self, partner):
        analytic_line_vals = super()._catch_values_for_create_analytic_line(partner)
        if self.event_id and self.event_id.organizer_id:
            analytic_line_vals["headquarter_id"] = self.event_id.organizer_id.id
        return analytic_line_vals
