# Copyright 2026 AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.tools import float_round

INCH_TO_MM = 25.4
SALE_LENGTH_ROUNDING = 0.05
SALE_WIDTH_ROUNDING = 0.125
MIN_SALE_WIDTH = 7.0
INCH_MM_FIELD_PAIRS = (
    ("length_mm", "length_in"),
    ("width_mm", "width_in"),
    ("wheelbase_mm", "wheelbase_in"),
    ("nose_mm", "nose_in"),
    ("tail_mm", "tail_in"),
)


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
        digits=(16, 3),
    )
    width_in = fields.Float(
        string="Width (in)",
        digits=(16, 3),
    )
    nose_in = fields.Float(
        string="Nose (in)",
        digits=(16, 3),
    )
    tail_in = fields.Float(
        string="Tail (in)",
        digits=(16, 3),
    )
    wheelbase_in = fields.Float(
        string="Wheelbase (in)",
        digits=(16, 3),
    )
    sale_length = fields.Float(digits=(16, 2))
    sale_width = fields.Float(digits=(16, 2))
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
    attribute_value_ids = fields.One2many(
        comodel_name="product.attribute.value",
        inverse_name="shape_id",
        string="Attribute Values",
    )
    attribute_value_count = fields.Integer(
        compute="_compute_attribute_value_count",
        store=True,
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

    @api.depends("attribute_value_ids")
    def _compute_attribute_value_count(self):
        for shape in self:
            shape.attribute_value_count = len(shape.attribute_value_ids)

    @api.onchange("length_in")
    def _onchange_length_in(self):
        self.length_mm = self.length_in * INCH_TO_MM

    @api.onchange("width_in")
    def _onchange_width_in(self):
        self.width_mm = self.width_in * INCH_TO_MM

    @api.onchange("wheelbase_in")
    def _onchange_wheelbase_in(self):
        self.wheelbase_mm = self.wheelbase_in * INCH_TO_MM

    @api.onchange("nose_in")
    def _onchange_nose_in(self):
        self.nose_mm = self.nose_in * INCH_TO_MM

    @api.onchange("tail_in")
    def _onchange_tail_in(self):
        self.tail_mm = self.tail_in * INCH_TO_MM

    @api.onchange("length_in")
    def _onchange_sale_length(self):
        self.sale_length = self._get_sale_length(self.length_in)

    @api.onchange("width_in")
    def _onchange_sale_width(self):
        self.sale_width = self._get_sale_width(self.width_in)

    @staticmethod
    def _get_sale_length(length_in):
        return float_round(length_in, precision_rounding=SALE_LENGTH_ROUNDING)

    @staticmethod
    def _get_sale_width(width_in):
        return float_round(
            max(width_in, MIN_SALE_WIDTH),
            precision_rounding=SALE_WIDTH_ROUNDING,
        )

    @classmethod
    def _fill_sale_measures(cls, vals):
        vals = dict(vals)
        if "length_in" in vals and "sale_length" not in vals:
            vals["sale_length"] = cls._get_sale_length(vals["length_in"] or 0.0)
        if "width_in" in vals and "sale_width" not in vals:
            vals["sale_width"] = cls._get_sale_width(vals["width_in"] or 0.0)
        return vals

    @staticmethod
    def _fill_missing_mm_measures(vals):
        vals = dict(vals)
        for mm_field, in_field in INCH_MM_FIELD_PAIRS:
            if vals.get(in_field) and not vals.get(mm_field):
                vals[mm_field] = vals[in_field] * INCH_TO_MM
        return vals

    @api.model_create_multi
    def create(self, vals_list):
        vals_list = [self._fill_missing_mm_measures(vals) for vals in vals_list]
        vals_list = [self._fill_sale_measures(vals) for vals in vals_list]
        for vals in vals_list:
            if vals.get("name"):
                vals["name"] = vals["name"].strip().upper()
        return super().create(vals_list)

    def write(self, vals):
        vals = self._fill_missing_mm_measures(vals)
        vals = self._fill_sale_measures(vals)
        if vals.get("name"):
            vals["name"] = vals["name"].strip().upper()
        return super().write(vals)
