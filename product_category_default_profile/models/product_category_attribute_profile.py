# Copyright 2026 Ane Gurruchaga - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductCategoryAttributeProfile(models.Model):
    _inherit = "product.category.attribute.profile"

    default_profile_product_id = fields.Many2one(
        comodel_name="product.product",
        string="Default Profile Product",
        domain="[('is_profile', '=', True)]",
    )
    bom_id = fields.Many2one(
        comodel_name="mrp.bom",
        string="Bill of Materials",
        compute="_compute_bom_id",
    )

    @api.depends(
        "default_profile_product_id",
        "default_profile_product_id.bom_ids",
        "default_profile_product_id.bom_ids.product_id",
    )
    def _compute_bom_id(self):
        for profile in self:
            product = profile.default_profile_product_id
            profile.bom_id = product.product_tmpl_id.bom_ids.filtered(
                lambda bom, product=product: (
                    not bom.product_id or bom.product_id == product
                )
            )[:1]
