# Copyright 2026 Ane Gurruchaga - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductShapeStyle(models.Model):
    _name = "product.shape.style"
    _description = "Product Shape Style"
    _order = "name"

    name = fields.Char(required=True, index=True)

    _sql_constraints = [
        ("name_unique", "unique(name)", "The shape style name must be unique."),
    ]
