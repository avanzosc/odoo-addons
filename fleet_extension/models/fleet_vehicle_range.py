# Copyright 2021 Berezi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class FleetVehicleRange(models.Model):
    _name = "fleet.vehicle.range"
    _description = "Vehicle Range"

    name = fields.Char(string="Name")
