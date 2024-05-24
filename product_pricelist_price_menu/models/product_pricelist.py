# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import _, fields, models


class ProductPricelist(models.Model):
    _inherit = "product.pricelist"

    def action_view_pricelist_product(self):
        context = self.env.context.copy()
        context.update({"pricelist_id": self.id})
        wiz = self.env["product.pricelist.print"].create({
            "pricelist_id": self.id,
            "date": fields.Date.today(),
            "show_only_defined_products": True
        })
        products = wiz.get_products_to_print()
        return {
            "name": _("Product Pricelist Price"),
            "view_mode": "tree",
            "view_id": self.env.ref(
                "product_pricelist_price_menu.product_template_pricelist_view_tree"
            ).id,
            "res_model": "product.template",
            "domain": [("id", "in", products.ids)],
            "type": "ir.actions.act_window",
            "context": context
        }
