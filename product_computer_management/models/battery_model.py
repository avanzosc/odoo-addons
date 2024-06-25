# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class BatteryModel(models.Model):
    _name = "battery.model"
    _description = "Battery Model"

    name = fields.Char(string="Name", required=True, copy=False)
