# Copyright 2019 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    restricted_products = fields.One2many(
        comodel_name="product.restrict", string="Restricted Products",
        inverse_name="product_id")
    product_restrictions = fields.One2many(
        comodel_name="product.restrict", string="Restricted Products",
        inverse_name="restricted_product_id")
    restricted_to_category = fields.Many2one(
        comodel_name="product.category",
        related="categ_id.category_restrict.restricted_to", store=True)
    restricted_for_category = fields.Many2one(
        comodel_name="product.category",
        related="categ_id.category_restrict.restricted_for", store=True)


class ProductRestrict(models.Model):
    _name = "product.restrict"
    _rec_name = "product_id"

    product_id = fields.Many2one(comodel_name="product.product",
                                 string="Product")
    restricted_product_id = fields.Many2one(
        comodel_name="product.product",
        string="Restricted Product", domain="[('categ_id', '=', "
        "categ_id.category_restrict.restricted_for)])")
