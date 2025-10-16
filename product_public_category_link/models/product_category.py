# Copyright 2025 Aner Arregi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProductCategory(models.Model):
    _inherit = "product.category"

    public_category_ids = fields.Many2many(
        "product.public.category",
        "product_category_public_category_rel",
        "category_id",
        "public_category_id",
        string="Public Categories",
        help="Public website categories associated with this internal category",
    )

    def write(self, vals):
        """Synchronize products when
        public categories change"""
        result = super().write(vals)

        if "public_category_ids" in vals:
            for category in self:
                products = self.env["product.template"].search(
                    [("categ_id", "=", category.id)]
                )

                if products:
                    current_product_categs = products.mapped("public_categ_ids")
                    new_categs = category.public_category_ids
                    categs_to_remove = current_product_categs - new_categs
                    categs_to_add = new_categs - current_product_categs

                    if categs_to_remove or categs_to_add:
                        for product in products:
                            if categs_to_remove:
                                product.write(
                                    {
                                        "public_categ_ids": [
                                            (3, cat.id) for cat in categs_to_remove
                                        ]
                                    }
                                )
                            if categs_to_add:
                                product.write(
                                    {
                                        "public_categ_ids": [
                                            (4, cat.id) for cat in categs_to_add
                                        ]
                                    }
                                )
        return result
