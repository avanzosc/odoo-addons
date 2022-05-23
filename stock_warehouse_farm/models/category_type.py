# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class CategoryType(models.Model):
    _name = "category.type"
    _description = "Category Type"

    name = fields.Char(
        string="Name",
        required=True,
    )

    _sql_constraints = [
        ("name_unique", "unique(name)", "Category Type name already exists"),
    ]
