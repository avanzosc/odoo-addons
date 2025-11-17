from odoo import fields, models


class CategoryDeleteWizard(models.TransientModel):
    _name = "category.delete.wizard"
    _description = "Category Delete Wizard"

    remove_public_categories = fields.Boolean(
        string="Remove public categories from products", default=False
    )

    def action_remove_public_categories(self):
        active_id = self.env.context.get("active_id")
        if active_id:
            category = self.env["product.category"].browse(active_id)
            if category.exists() and self.remove_public_categories:
                products = self.env["product.template"].search(
                    [("categ_id", "=", category.id)]
                )
                if products:
                    products.write({"public_categ_ids": [(5, 0, 0)]})
                category.write({"public_category": [(5, 0, 0)]})

        return {
            "type": "ir.actions.act_window_close",
            "effect": {
                "type": "rainbow_man",
                "message": "Public categories updated successfully!",
            },
        }
