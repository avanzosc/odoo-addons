# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    manual_standard_cost = fields.Float(
        compute="_compute_manual_standard_cost",
        digits="Product Price",
        inverse="_inverse_manual_standard_cost",
    )

    @api.depends("product_tmpl_id", "product_tmpl_id.manual_standard_cost")
    def _compute_manual_standard_cost(self):
        for product in self:
            if product.product_tmpl_id.product_variant_count == 1:
                product.manual_standard_cost = (
                    product.product_tmpl_id.manual_standard_cost
                )

    @api.onchange("manual_standard_cost")
    def _inverse_manual_standard_cost(self):
        for product in self:
            value = product.manual_standard_cost
            if product.product_tmpl_id.product_variant_count == 1:
                product.product_tmpl_id.write({"manual_standard_cost": value})
