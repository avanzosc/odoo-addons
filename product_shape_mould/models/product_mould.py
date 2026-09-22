# Copyright 2026 AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductMould(models.Model):
    _name = "product.mould"
    _description = "Mould / Template"
    _order = "name"

    type = fields.Selection(
        selection=[
            ("mould", "Mould"),
            ("template", "Template"),
        ],
        required=True,
        default="mould",
        index=True,
    )
    name = fields.Char(required=True, index=True)
    group = fields.Char()
    subgroup = fields.Char()
    description = fields.Text()
    manufacturing_year = fields.Integer()
    modification_year = fields.Integer()
    mould_id = fields.Many2one(
        comodel_name="product.mould",
        domain=[("type", "=", "mould")],
    )

    _sql_constraints = [
        ("code_unique", "unique(name)", "The mould name must be unique."),
    ]
