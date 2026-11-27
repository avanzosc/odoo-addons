# Copyright 2026 AvanzOSC - Lucía Echeverría
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProductAttribute(models.Model):
    _inherit = "product.attribute"

    shop_variant_split = fields.Boolean(
        string="Split variants in shop",
        help="In the online shop, products with 'Split variants in shop' "
        "show a separate product for each value of this attribute.",
    )
