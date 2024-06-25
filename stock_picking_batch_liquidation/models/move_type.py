# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class MoveType(models.Model):
    _name = "move.type"
    _description = "Move Type"

    name = fields.Char(string="Name")
