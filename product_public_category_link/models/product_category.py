# Copyright 2025 Aner Arregi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductCategory(models.Model):
    _inherit = "product.category"

    public_category = fields.Many2many(
        "product.public.category",
        "product_category_publiccategory_rel",
        "category_id",
        "public_category_id",
        string="Public Categories",
    )

    def action_remove_public_categories(self):
        products = self.env["product.template"].search([("categ_id", "in", self.ids)])
        products.write({"public_categ_ids": [(5, 0, 0)]})
        self.write({"public_category": [(5, 0, 0)]})
