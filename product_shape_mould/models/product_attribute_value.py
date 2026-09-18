# Copyright 2026 Ana Juaristi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


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
