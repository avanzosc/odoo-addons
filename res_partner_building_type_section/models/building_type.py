# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class BuildingType(models.Model):
    _name = "building.type"
    _description = "Building type"

    name = fields.Char(string="Description", required=True, copy=False)
