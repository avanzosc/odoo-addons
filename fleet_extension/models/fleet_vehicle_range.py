# Copyright 2021 Berezi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class FleetVehicleRange(models.Model):
    _name = 'fleet.vehicle.range'
    _description = 'Vehicle Range'

    name = fields.Char(string='Name')
