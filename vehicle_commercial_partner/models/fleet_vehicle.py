# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class FleetVehicle(models.Model):
    _inherit = "fleet.vehicle"

    commercial_partner_id = fields.Many2one(
        string="Commercial Partner",
        comodel_name="res.partner",
        compute="_compute_commercial_partner",
        store=True)

    @api.depends("driver_id")
    def _compute_commercial_partner(self):
        for vehicle in self:
            vehicle.commercial_partner_id = vehicle.driver_id.id
            if vehicle.driver_id.company_type == "person":
                vehicle.commercial_partner_id = vehicle.driver_id.parent_id.id
