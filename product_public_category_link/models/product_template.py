# Copyright 2025 Aner Arregi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    public_categ_ids = fields.Many2many(
        "product.public.category",
        "product_public_category_rel",
        "product_tmpl_id",
        "public_category_id",
        string="Public Categories",
        help="Public website categories associated with this product",
    )

    @api.model_create_multi
    def create(self, vals_list):
        """Override create to automatically add
        public categories from product category"""
        records = super().create(vals_list)

        for record in records:
            if record.categ_id and record.categ_id.public_category_ids:
                record._sync_public_categories_from_category(
                    record.categ_id.public_category_ids
                )

        return records

    def write(self, vals):
        """Override write to sync public
        categories when category changes"""
        res = super().write(vals)

        if "categ_id" in vals:
            for record in self:
                if record.categ_id and record.categ_id.public_category_ids:
                    record._sync_public_categories_from_category(
                        record.categ_id.public_category_ids
                    )

        return res

    def _sync_public_categories_from_category(self, new_public_categories):
        """Sync public categories from product
        category to product template"""
        self.ensure_one()
        current_public_categories = self.public_categ_ids
        categories_to_add = new_public_categories - current_public_categories
        if categories_to_add:
            self.write({"public_categ_ids": [(4, cat.id) for cat in categories_to_add]})
