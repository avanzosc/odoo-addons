# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class ProductPricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    product_default_code = fields.Char(string="Product Internal Reference", copy=False)

    @api.onchange("product_id")
    def _onchange_product_id(self):
        result = super()._onchange_product_id()
        product_default_code = ""
        if self.product_id and self.product_id.default_code:
            product_default_code = self.product_id.default_code
        self.product_default_code = product_default_code
        return result

    @api.onchange("product_tmpl_id")
    def _onchange_product_tmpl_id(self):
        result = super()._onchange_product_tmpl_id()
        product_default_code = ""
        if self.product_tmpl_id and self.product_tmpl_id.default_code:
            product_default_code = self.product_tmpl_id.default_code
        self.product_default_code = product_default_code
        return result

    @api.depends(
        "product_tmpl_id",
        "product_tmpl_id.default_code",
        "product_id",
        "product_id.default_code",
    )
    def _compute_product_default_code(self):
        for item in self:
            product_default_code = ""
            if item.product_id and item.product_id.default_code:
                product_default_code = item.product_id.default_code
            else:
                if item.product_tmpl_id and item.product_tmpl_id.default_code:
                    product_default_code = item.product_tmpl_id.default_code
            item.product_default_code = product_default_code
