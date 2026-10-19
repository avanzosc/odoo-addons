# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class ProductPackaging(models.Model):
    _inherit = "product.packaging"

    package_type_id = fields.Many2one(required=True)

    def write(self, vals):
        res = super().write(vals)
        if not self.env.context.get("skip_packaging_weight_height_recompute") and (
            "package_type_id" in vals or "qty" in vals
        ):
            self.mapped("product_id").action_recalculate_packaging_weight_height()
        return res

    @api.model_create_multi
    def create(self, vals_list):
        packagings = super().create(vals_list)
        if not self.env.context.get("skip_packaging_weight_height_recompute"):
            packagings.mapped("product_id").action_recalculate_packaging_weight_height()
        return packagings
