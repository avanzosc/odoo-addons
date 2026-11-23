# Copyright 2026 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models

PRICING_METHOD_SELECTION = [
    ("qty", "Quantity"),
    ("weight", "Weight"),
    ("length", "Length"),
    ("wl", "Weight*Length"),
]


class ProductCategory(models.Model):
    _inherit = "product.category"

    dim_order_method = fields.Selection(
        selection=[
            ("lhw", "Length, Height, Width"),
            ("lwh", "Length, Width, Heigh"),
            ("wlh", "Width, Length, Height"),
            ("whl", "Width, Height, Length"),
            ("hlw", "Height, Length, Width"),
            ("hwl", "Height, Width, Length"),
        ],
        default="lhw",
    )
    pricing_method = fields.Selection(
        selection=PRICING_METHOD_SELECTION,
        default="qty",
        help="Default pricing method for the products of this category. "
        "Changing it updates the pricing method of all the products of the "
        "category.",
    )
