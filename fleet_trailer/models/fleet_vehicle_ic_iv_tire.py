# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class FleetVehicleIcIvTire(models.Model):
    _name = 'fleet.vehicle.ic.iv.tire'
    _description = 'IC/IV tires'

    name = fields.Char(string='Description')
