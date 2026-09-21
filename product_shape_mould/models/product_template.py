# Copyright 2026 AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_mould = fields.Boolean(string="Is a Mould")

    def action_unify_shape_attributes(self):
        for template in self:
            if len(template.with_context(active_test=False).product_variant_ids) != 1:
                continue
            shape = template._get_attribute_shape()
            if not shape:
                continue
            for mapping in shape.attribute_mapping_ids:
                value_name = template._get_shape_attribute_value_name(
                    shape, mapping.shape_field_id
                )
                if not value_name:
                    continue
                attribute_value = template._get_or_create_attribute_value(
                    mapping.attribute_id, value_name
                )
                template._set_attribute_line_value(
                    mapping.attribute_id, attribute_value
                )

    def _get_attribute_shape(self):
        self.ensure_one()
        shape_values = self.attribute_line_ids.filtered(
            lambda line: line.attribute_id.is_shape
        ).value_ids.filtered("shape_id")
        return shape_values[:1].shape_id

    def _get_shape_attribute_value_name(self, shape, shape_field):
        self.ensure_one()
        value = shape[shape_field.name]
        if not value:
            return False
        if shape_field.ttype == "many2one":
            return value.display_name
        if shape_field.ttype == "float":
            return f"{value:g}"
        return str(value)

    def _get_or_create_attribute_value(self, attribute, value_name):
        self.ensure_one()
        attribute_value = self.env["product.attribute.value"].search(
            [
                ("attribute_id", "=", attribute.id),
                ("name", "=", value_name),
            ],
            limit=1,
        )
        if not attribute_value:
            attribute_value = self.env["product.attribute.value"].create(
                {
                    "attribute_id": attribute.id,
                    "name": value_name,
                }
            )
        return attribute_value

    def _set_attribute_line_value(self, attribute, attribute_value):
        self.ensure_one()
        line = self.attribute_line_ids.filtered(
            lambda attribute_line: attribute_line.attribute_id == attribute
        )[:1]
        if line:
            line.value_ids = [(6, 0, attribute_value.ids)]
        else:
            self.attribute_line_ids = [
                (
                    0,
                    0,
                    {
                        "attribute_id": attribute.id,
                        "value_ids": [(6, 0, attribute_value.ids)],
                    },
                )
            ]
