# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class WaterSubactivity(models.Model):
    _name = "water.subactivity"
    _description = "Contacts Water Subactivity"

    name = fields.Char(required=True, copy=False)
    water = fields.Boolean(default=False, copy=False)
    industry = fields.Boolean(default=False, copy=False)
