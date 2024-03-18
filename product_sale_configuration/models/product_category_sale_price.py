# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import _, api, fields, models


class ProductCategorySalePrice(models.Model):
    _name = "product.category.sale.price"
    _description = "Product category sale price"
    _order = "sequence, id"

    name = fields.Char(string="Name", required=True)
    percentage = fields.Float(string="% Increase", default=0.0)
    fixed_amount = fields.Float(string="Fixed amount")
    product_ids = fields.One2many(
        string="Products",
        comodel_name="product.product",
        inverse_name="product_category_sale_price_id",
    )
    count_products = fields.Integer(
        string="Products", compute="_compute_count_products"
    )
    sequence = fields.Integer(string="Sequence", default=10)

    def _compute_count_products(self):
        for cat in self:
            cat.count_products = len(cat.product_ids)

    def name_get(self):
        res = []
        for price in self:
            name = _("{}: % Increment: {}, Fixed amount: {}").format(
                price.name, price.percentage, price.fixed_amount
            )
            res.append((price.id, name))
        return res

    def button_show_products(self):
        self.ensure_one()
        return {
            "name": _("Products"),
            "type": "ir.actions.act_window",
            "view_mode": "tree,form,kanban,activity",
            "view_type": "form",
            "res_model": "product.product",
            "domain": [("id", "in", self.product_ids.ids)],
        }

    def write(self, vals):
        result = super().write(vals)
        if "percentage" in vals or "fixed_amount" in vals:
            for category in self:
                category.product_ids._onchange_category_sale_price()
        return result
