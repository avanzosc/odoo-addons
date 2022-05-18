# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class Coya(models.Model):
    _name = "coya"
    _description = "Coya"

    name = fields.Char(string='Name', required=True)
