# Copyright 2021 Berezi - Iker - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class FleetVehicleModelType(models.Model):
    _name = 'fleet.vehicle.model.type'
    _description = 'Vehicle type'

    name = fields.Char(string='Type')
