# Copyright 2026 AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductShape(models.Model):
    _name = "product.shape"
    _description = "Product Shape"
    _order = "name"

    brand_info = fields.Char(index=True)
    name = fields.Char(
        string="Shape",
        required=True,
    )
    mould_id = fields.Many2one(
        comodel_name="product.mould",
        string="Mould",
        compute="_compute_mould_id",
        store=True,
    )
    template_id = fields.Many2one(
        comodel_name="product.mould",
        string="Template",
        domain=[("type", "=", "template")],
    )
    similar_shape_id = fields.Many2one(
        comodel_name="product.shape",
        string="Similar To",
    )
    customer_table_ref = fields.Char(string="Customer Table Reference")
    comments = fields.Text()
    length_mm = fields.Float(
        string="Length (mm)",
    )
    width_mm = fields.Float(
        string="Width (mm)",
    )
    nose_mm = fields.Float(
        string="Nose (mm)",
    )
    tail_mm = fields.Float(
        string="Tail (mm)",
    )
    wheelbase_mm = fields.Float(
        string="Wheelbase (mm)",
    )
    length_in = fields.Float(
        string="Length (in)",
    )
    width_in = fields.Float(
        string="Width (in)",
    )
    nose_in = fields.Float(
        string="Nose (in)",
    )
    tail_in = fields.Float(
        string="Tail (in)",
    )
    wheelbase_in = fields.Float(
        string="Wheelbase (in)",
    )
    wheel_well_recesses = fields.Boolean()
    double_wheelbase = fields.Boolean()
    symmetric = fields.Boolean(compute="_compute_symmetric", store=True)
    drop = fields.Boolean()
    exclusive = fields.Boolean()
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        default=lambda self: self.env.company,
    )

    _sql_constraints = [
        (
            "code_unique",
            "unique(name)",
            "The shape name must be unique.",
        ),
    ]

    @api.depends("name")
    def _compute_mould_id(self):
        for shape in self:
            mould_name = shape.name[:3] if shape.name else False
            shape.mould_id = self.env["product.mould"].search(
                [
                    ("name", "=", mould_name),
                    ("type", "=", "mould"),
                ],
                limit=1,
            )

    @api.depends("nose_mm", "tail_mm")
    def _compute_symmetric(self):
        for shape in self:
            shape.symmetric = shape.nose_mm == shape.tail_mm

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name"):
                vals["name"] = vals["name"].strip().upper()
        return super().create(vals_list)

    def write(self, vals):
        if vals.get("name"):
            vals["name"] = vals["name"].strip().upper()
        return super().write(vals)
