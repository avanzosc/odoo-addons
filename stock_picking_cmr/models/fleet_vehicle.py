# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class FleetVehicle(models.Model):
    _inherit = "fleet.vehicle"

    special_traffic_authorization = fields.Boolean(
        default=False,
        copy=False,
    )
