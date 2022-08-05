# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class FleetVehicleModelType(models.Model):
    _inherit = "fleet.vehicle.model.type"

    category = fields.Selection(
        string="Category",
        selection=[
            ("head", "Head"),
            ("trailer", "Trailer"),
            ("other", "Other")],
        copy=False)
