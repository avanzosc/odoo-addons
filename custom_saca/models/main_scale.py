# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class MainScale(models.Model):
    _name = "main.scale"
    _description = "Main Scale"

    name = fields.Char(string='Name', required=True)
