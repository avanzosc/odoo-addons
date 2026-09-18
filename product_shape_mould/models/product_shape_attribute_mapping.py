# Copyright 2026 Ana Juaristi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductShapeAttributeMapping(models.Model):
    _name = "product.shape.attribute.mapping"
    _description = "Product Shape Attribute Mapping"

    shape_id = fields.Many2one(
        comodel_name="product.shape",
        required=True,
        ondelete="cascade",
    )
    shape_field_id = fields.Many2one(
        comodel_name="ir.model.fields",
        string="Shape Field",
        domain=[("model", "=", "product.shape")],
        required=True,
        ondelete="cascade",
    )
    attribute_id = fields.Many2one(
        comodel_name="product.attribute",
        string="Attribute",
        required=True,
        ondelete="cascade",
    )
