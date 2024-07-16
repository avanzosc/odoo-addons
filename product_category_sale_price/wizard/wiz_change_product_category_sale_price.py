# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class WizChangeProductCategorySalePrice(models.TransientModel):
    _name = "wiz.change.product.category.sale.price"
    _description = "Wizard for change product category sale price in products"

    category_id = fields.Many2one(
        string="Product category sale price", comodel_name="product.category.sale.price"
    )

    def button_change_category(self):
        context = dict(self._context or {})
        active_ids = context.get("active_ids", []) or []
        products = self.env["product.product"].browse(active_ids)
        if products:
            products.write({"product_category_sale_price_id": self.category_id.id})
            products._onchange_category_sale_price()
        return {"type": "ir.actions.act_window_close"}
