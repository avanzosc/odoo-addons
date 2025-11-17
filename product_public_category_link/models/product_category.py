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

    def open_remove_public_wizard(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Remove Public Categories",
            "res_model": "category.delete.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {"active_id": self.id},
        }

    def write(self, vals):
        result = super().write(vals)

        if "public_category" in vals:
            new_public_categories = vals["public_category"]
            if new_public_categories and any(
                op[0] in [4, 6, 1]
                for op in new_public_categories
                if isinstance(op, list)
            ):
                for category in self:
                    products = self.env["product.template"].search(
                        [("categ_id", "=", category.id)]
                    )
                    if products:
                        products.write(
                            {"public_categ_ids": [(6, 0, category.public_category.ids)]}
                        )

        return result
