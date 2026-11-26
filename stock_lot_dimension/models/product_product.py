# Copyright 2026 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    product_length = fields.Float(digits="Product Dimension")
    product_height = fields.Float(digits="Product Dimension")
    product_width = fields.Float(digits="Product Dimension")
    weight = fields.Float(digits="Product Dimension Weight")
