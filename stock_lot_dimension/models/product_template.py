# Copyright 2026 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models

from .product_category import PRICING_METHOD_SELECTION


class ProductTemplate(models.Model):
    _inherit = "product.template"

    pricing_method = fields.Selection(
        selection=PRICING_METHOD_SELECTION,
        compute="_compute_pricing_method",
        store=True,
        readonly=False,
        precompute=True,
        help="Taken from the product category. It can be changed for this "
        "product, but it is updated again when the pricing method of the "
        "category changes.",
    )

    product_length = fields.Float(digits="Product Dimension")
    product_height = fields.Float(digits="Product Dimension")
    product_width = fields.Float(digits="Product Dimension")
    weight = fields.Float(digits="Product Dimension Weight")

    dim_order_method = fields.Selection(
        related="categ_id.dim_order_method",
        readonly=True,
        store=True,
    )

    @api.depends("categ_id", "categ_id.pricing_method")
    def _compute_pricing_method(self):
        for template in self:
            template.pricing_method = template.categ_id.pricing_method or "qty"
