# Copyright 2026 Ana Juaristi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class OdooVersion(models.Model):
    _name = "odoo.version"
    _description = "Odoo Version"
    _order = "sequence, name"

    name = fields.Char(required=True)
    sequence = fields.Integer(default=10)

    _sql_constraints = [
        ("name_uniq", "unique(name)", "Odoo version name must be unique."),
    ]
