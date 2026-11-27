# Copyright 2026 AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.depends(
        "product_tmpl_id.product_variant_ids",
        "product_template_attribute_value_ids.attribute_id.code",
        "product_template_attribute_value_ids.product_attribute_value_id.code",
    )
    def _compute_default_code(self):
        products_with_variants = self.filtered(
            lambda product: product.product_tmpl_id.product_variant_count > 1
        )
        return super(ProductProduct, products_with_variants)._compute_default_code()
