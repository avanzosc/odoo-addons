# Copyright 2026 Berezi Amubieta - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class GrantProgram(models.Model):
    _name = "grant.program"
    _description = "Linea Subvencional"

    name = fields.Char(
        string="Descripción",
        required=True,
    )
