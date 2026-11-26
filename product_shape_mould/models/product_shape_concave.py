# Copyright 2026 Ane Gurruchaga - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductShapeConcave(models.Model):
    _name = "product.shape.concave"
    _description = "Product Shape Concave"
    _order = "name"

    name = fields.Char(required=True, index=True)

    _sql_constraints = [
        ("name_unique", "unique(name)", "The concave name must be unique."),
    ]
