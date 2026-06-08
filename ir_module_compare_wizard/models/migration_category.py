# Copyright 2026 Alfredo de la Fuente, Ana Juaristi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class MigrationCategory(models.Model):
    _name = "migration.category"
    _description = "Migration Categories"

    name = fields.Char(string="Description")
