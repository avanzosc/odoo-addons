# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import _, models


class ProductPricelist(models.Model):
    _inherit = "product.pricelist"

    def action_view_items(self):
        context = self.env.context.copy()
        context.update({"default_pricelist_id": self.id})
        return {
            "name": _("Items"),
            "view_mode": "tree",
            "views": [
                [
                    self.env.ref(
                        "product.product_pricelist_item_tree_view_from_product"
                    ).id,
                    "tree",
                ]
            ],
            "res_model": "product.pricelist.item",
            "domain": [("id", "in", self.item_ids.ids)],
            "type": "ir.actions.act_window",
            "context": context,
        }
