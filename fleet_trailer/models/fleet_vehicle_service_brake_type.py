# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class FleetVehicleServiceBrakeType(models.Model):
    _name = 'fleet.vehicle.service.brake.type'
    _description = 'Vehicle service brake type'

    name = fields.Char(string='Description')
