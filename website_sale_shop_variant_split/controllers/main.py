# Copyright 2026 AvanzOSC - Lucía Echeverría
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from collections import Counter

from odoo.http import route
from odoo.tools import lazy

from odoo.addons.website_sale.controllers.main import TableCompute, WebsiteSale


class WebsiteSaleShopVariantSplit(WebsiteSale):
    def _shop_lookup_products(self, attrib_set, options, post, search, website):
        fuzzy_search_term, product_count, search_result = super()._shop_lookup_products(
            attrib_set, options, post, search, website
        )
        split_variants = search_result._get_shop_split_variants(attrib_set)
        if split_variants:
            template_ids = []
            for template_id in search_result.ids:
                template_ids += [template_id] * len(
                    split_variants.get(template_id, [template_id])
                )
            product_count += len(template_ids) - len(search_result)
            search_result = search_result.browse(template_ids)
        return fuzzy_search_term, product_count, search_result

    @route()
    def shop(
        self,
        page=0,
        category=None,
        search="",
        min_price=0.0,
        max_price=0.0,
        ppg=False,
        **post,
    ):
        response = super().shop(
            page=page,
            category=category,
            search=search,
            min_price=min_price,
            max_price=max_price,
            ppg=ppg,
            **post,
        )
        values = getattr(response, "qcontext", {})
        products = values.get("products")
        if not products:
            return response
        split_variants = products._get_shop_split_variants(values["attrib_set"])
        if not split_variants:
            return response
        shown = Counter(values["search_product"].ids[: values["pager"]["offset"]])
        cards = []
        for product in products:
            variants = split_variants.get(product.id)
            if variants:
                variant = variants[min(shown[product.id], len(variants) - 1)]
                shown[product.id] += 1
                product = product.with_context(shop_split_variant_id=variant.id)
            cards.append(product)
        values["bins"] = lazy(
            lambda: TableCompute().process(cards, values["ppg"], values["ppr"])
        )
        get_product_prices = values["get_product_prices"]
        values["get_product_prices"] = lambda product: (
            lazy(product._get_shop_split_prices)
            if product._get_shop_split_variant()
            else get_product_prices(product)
        )
        return response
