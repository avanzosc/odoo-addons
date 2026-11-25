# Copyright 2026 Ane Gurruchaga - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductCategoryAttributeProfile(models.Model):
    _name = "product.category.attribute.profile"
    _description = "Product Category Attribute Profile"
    _order = "name"

    name = fields.Char(required=True)
    attribute_ids = fields.Many2many(
        comodel_name="product.attribute",
        relation="product_category_attribute_profile_attribute_rel",
        column1="profile_id",
        column2="attribute_id",
        string="Attributes",
    )
    category_ids = fields.One2many(
        comodel_name="product.category",
        inverse_name="attribute_profile_id",
        string="Included Categories",
    )


class ProductCategory(models.Model):
    _inherit = "product.category"

    attribute_profile_id = fields.Many2one(
        comodel_name="product.category.attribute.profile",
        string="Attribute Profile",
        ondelete="restrict",
    )
