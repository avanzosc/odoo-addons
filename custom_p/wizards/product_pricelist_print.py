# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models
from odoo.osv import expression


class ProductPricelistPrint(models.TransientModel):
    _inherit = "product.pricelist.print"

    show_only_defined_products = fields.Boolean(
        default=True
    )

    def get_products_domain(self):
        domain = super(ProductPricelistPrint, self).get_products_domain()
        if self.show_only_defined_products:
            domain = [("sale_ok", "=", True)]
            aux_domain = []
            items_dic = {"categ_ids": [], "product_ids": [], "variant_ids": []}
            items = self.pricelist_id.item_ids + self.pricelist_id.item_ids.base_pricelist_id.item_ids
            for item in items:
                if item.base_pricelist_id:
                    items += item.base_pricelist_id.item_ids
            for item in items:
                if item.applied_on == "0_product_variant":
                    items_dic["variant_ids"].append(item.product_id.id)
                if item.applied_on == "1_product":
                    items_dic["product_ids"].append(item.product_tmpl_id.id)
                if item.applied_on == "2_product_category" and item.categ_id.parent_id:
                    items_dic["categ_ids"].append(item.categ_id.id)
            if items_dic["categ_ids"]:
                aux_domain = expression.OR(
                    [aux_domain, [("categ_id", "in", items_dic["categ_ids"])]]
                )
            if items_dic["product_ids"]:
                if self.show_variants:
                    aux_domain = expression.OR(
                        [
                            aux_domain,
                            [("product_tmpl_id", "in", items_dic["product_ids"])],
                        ]
                    )
                else:
                    aux_domain = expression.OR(
                        [aux_domain, [("id", "in", items_dic["product_ids"])]]
                    )
            if items_dic["variant_ids"]:
                if self.show_variants:
                    aux_domain = expression.OR(
                        [aux_domain, [("id", "in", items_dic["variant_ids"])]]
                    )
                else:
                    aux_domain = expression.OR(
                        [
                            aux_domain,
                            [("product_variant_ids", "in", items_dic["variant_ids"])],
                        ]
                    )
            domain = expression.AND([domain, aux_domain])
        if self.categ_ids:
            domain = expression.AND([domain, [("categ_id", "in", self.categ_ids.ids)]])
        return domain
