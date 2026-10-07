# Copyright 2026 Ana Juaristi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"

    attribute_is_shape = fields.Boolean(
        related="attribute_id.is_shape",
        string="Shape Attribute",
        store=True,
    )
    shape_id = fields.Many2one(
        comodel_name="product.shape",
        string="Shape",
    )
    mould_id = fields.Many2one(
        comodel_name="product.mould",
        related="shape_id.mould_id",
        string="Mould",
        store=True,
    )
    shape_match_state = fields.Selection(
        selection=[
            ("ok", "Correct"),
            ("not_found", "Incorrect: Does Not Exist"),
            ("duplicated", "Incorrect: Duplicated"),
        ],
        string="Shape Match Status",
    )

    @api.onchange("shape_id")
    def _onchange_shape_id(self):
        for value in self:
            value._update_shape_values()

    @api.constrains("attribute_id", "shape_id")
    def _check_shape_id(self):
        for value in self:
            if not value.attribute_id.is_shape:
                continue
            if not value.shape_id:
                raise ValidationError(
                    _("Shape is required for shape attribute values.")
                )
            domain = [
                ("id", "!=", value.id),
                ("attribute_id", "=", value.attribute_id.id),
                ("shape_id", "=", value.shape_id.id),
            ]
            if self.search_count(domain):
                raise ValidationError(
                    _("This shape is already used by another attribute value.")
                )

    @api.model_create_multi
    def create(self, vals_list):
        vals_list = [self._prepare_shape_values(vals) for vals in vals_list]
        return super().create(vals_list)

    def write(self, vals):
        for value in self:
            super(ProductAttributeValue, value).write(value._prepare_shape_values(vals))
        return True

    def action_link_shape_values(self):
        shape_attributes = self.env["product.attribute"].search(
            [("is_shape", "=", True)]
        )
        values = self.search([("attribute_id", "in", shape_attributes.ids)])
        used_shapes = self.env["product.shape"]
        for value in values:
            shapes = self.env["product.shape"].search([("name", "=", value.name)])
            if not shapes:
                value.shape_match_state = "not_found"
            elif len(shapes) > 1 or shapes in used_shapes:
                value.shape_match_state = "duplicated"
            else:
                value.write(
                    {
                        "shape_id": shapes.id,
                        "shape_match_state": "ok",
                    }
                )
                used_shapes |= shapes

    def _prepare_shape_values(self, vals):
        vals = dict(vals)
        attribute = self.attribute_id
        if vals.get("attribute_id"):
            attribute = self.env["product.attribute"].browse(vals["attribute_id"])
        shape = self.shape_id
        if vals.get("shape_id"):
            shape = self.env["product.shape"].browse(vals["shape_id"])
        if attribute.is_shape and shape:
            vals["name"] = shape.name
            if "code" in self._fields:
                vals["code"] = shape.name
        return vals

    def _update_shape_values(self):
        self.ensure_one()
        if self.shape_id:
            self.name = self.shape_id.name
            if "code" in self._fields:
                self.code = self.shape_id.name
