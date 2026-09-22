# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import re

from odoo import api, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.depends("name", "default_code", "product_tmpl_id")
    @api.depends_context(
        "display_default_code", "seller_id", "company_id", "partner_id", "lang"
    )
    def _compute_display_name(self):
        result = super()._compute_display_name()
        for product in self:
            if product.default_code and not re.search(
                r"[A-Za-z0-9]", product.default_code
            ):
                product.display_name = product.display_name.replace(
                    f"[{product.default_code}] ",
                    "",
                )
        return result
