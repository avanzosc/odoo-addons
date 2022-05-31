# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class FleetVehicleTireDimension(models.Model):
    _name = 'fleet.vehicle.tire.dimension'
    _description = 'Vehicle tire dimension'

    name = fields.Char(string='Description')
