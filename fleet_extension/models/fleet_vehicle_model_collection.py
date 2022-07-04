# Copyright 2021 Berezi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class FleetVehicleModelCollection(models.Model):
    _name = "fleet.vehicle.model.collection"
    _description = "Vehicle collection"

    name = fields.Char(string="Collection")
