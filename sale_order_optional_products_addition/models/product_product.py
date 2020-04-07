# Copyright 2020 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    optional_product_product_ids = fields.Many2many(
        column1="product_id", column2="option_id",
        relation="product_product_optional_rel", comodel_name="product.product",
        string="Variant Optional Products")
