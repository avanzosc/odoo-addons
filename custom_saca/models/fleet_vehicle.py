# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class FleetVehicle(models.Model):
    _inherit = "fleet.vehicle"

    cages_num = fields.Integer(string='Number of Cages')
    max_weight = fields.Float(string='Max Weight')
    ates = fields.Char(string='Ates')
