# Copyright 2021 Berezi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class FleetVehicleModel(models.Model):
    _inherit = "fleet.vehicle.model"

    type_id = fields.Many2one(
        string="Vehicle type", comodel_name="fleet.vehicle.model.type"
    )
