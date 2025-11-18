# Copyright 2025 Aner Arregi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def write(self, vals):
        result = super().write(vals)
        if "categ_id" in vals:
            for product in self:
                product.public_categ_ids = (
                    product.categ_id.public_category if product.categ_id else False
                )
        return result

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for product in records:
            if product.categ_id and product.categ_id.public_category:
                product.public_categ_ids = product.categ_id.public_category
        return records

    @api.onchange("categ_id")
    def _onchange_categ_id_sync_public_categories(self):
        self.public_categ_ids = (
            self.categ_id.public_category if self.categ_id else False
        )
