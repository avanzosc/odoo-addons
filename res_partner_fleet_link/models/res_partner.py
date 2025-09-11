# Copyright 2025 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    vehicle_count = fields.Integer(
        string="Vehículos", compute="_compute_vehicle_count", readonly=True
    )

    def _compute_vehicle_count(self):
        for partner in self:
            partner.vehicle_count = self.env["fleet.vehicle"].search_count(
                [("driver_id", "=", partner.id)]
            )

    def action_view_partner_vehicles(self):
        self.ensure_one()
        return {
            "name": "Vehículos",
            "type": "ir.actions.act_window",
            "res_model": "fleet.vehicle",
            "view_mode": "tree,form",
            "domain": [("driver_id", "=", self.id)],
            "context": {"default_driver_id": self.id},
        }
