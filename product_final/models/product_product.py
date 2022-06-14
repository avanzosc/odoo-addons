# Copyright 2022 Patxi Lersundi
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    product_final_ids = fields.One2many(
                                comodel_name='product.location.exploded',
                                string="Final products",
                                inverse_name="product_id")
