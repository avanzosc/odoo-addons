# Copyright 2026 Ane Gurruchaga - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductCategory(models.Model):
    _inherit = "product.category"

    default_profile_product_id = fields.Many2one(
        comodel_name="product.product",
        string="Default Profile Product",
        domain="[('is_profile', '=', True)]",
        ondelete="restrict",
    )
