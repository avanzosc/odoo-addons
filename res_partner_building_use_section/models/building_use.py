# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class BuildingUse(models.Model):
    _name = "building.use"
    _description = "Building use"

    name = fields.Char(
        string="Description", required=True, copy=False
    )
    is_industrial = fields.Boolean(string="Industrial")
