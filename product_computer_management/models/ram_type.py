# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class RamType(models.Model):
    _name = "ram.type"
    _description = "Ram Type"

    name = fields.Char(string="Name", required=True, copy=False)
