# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class ProductPricelistItem(models.Model):
    _inherit = "product.pricelist.item"
    _order = "product_default_code asc, applied_on, min_quantity desc, categ_id desc, id desc"

    product_default_code = fields.Char(
        string="Product Internal Reference",
        compute="_compute_product_default_code", store=True, copy=False
    )

    @api.depends("product_tmpl_id", "product_tmpl_id.default_code",
                 "product_id", "product_id.default_code")
    def _compute_product_default_code(self):
        for item in self:
            product_default_code = ""
            if item.product_id and item.product_id.default_code:
                product_default_code = item.product_id.default_code
            else:
                if item.product_tmpl_id and item.product_tmpl_id.default_code:
                    product_default_code = item.product_tmpl_id.default_code
            item.product_default_code = product_default_code
