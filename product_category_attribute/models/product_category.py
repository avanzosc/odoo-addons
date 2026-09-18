# Copyright 2026 Ane Gurruchaga - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductCategory(models.Model):
    _inherit = "product.category"

    allowed_attribute_ids = fields.Many2many(
        comodel_name="product.attribute",
        relation="product_category_allowed_attribute_rel",
        column1="category_id",
        column2="attribute_id",
        string="Allowed Attributes",
    )
