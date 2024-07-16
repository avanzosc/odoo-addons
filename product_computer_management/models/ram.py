# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class Ram(models.Model):
    _name = "ram"
    _description = "Ram"

    name = fields.Char(string="Name", required=True, copy=False)
