from odoo import http
from odoo.http import request

from odoo.addons.website_sale.controllers.main import TableCompute, WebsiteSale


class CustomWebsiteSale(WebsiteSale):

    @http.route()
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
        res = super().shop(
            page=page,
            category=category,
            search=search,
            min_price=min_price,
            max_price=max_price,
            ppg=ppg,
            **post,
        )

        partner = request.env.user.partner_id
        permitted_category_ids = partner.permitted_web_categories.ids

        if permitted_category_ids:
            filtered_categories = res.qcontext["categories"].filtered(
                lambda categ: categ.id in permitted_category_ids
            )
            res.qcontext.update({"categories": filtered_categories})

            filtered_search_products = res.qcontext["search_product"].filtered(
                lambda prod: prod.public_categ_ids.filtered(
                    lambda categ: categ.id in permitted_category_ids
                )
            )

            filtered_products = res.qcontext["products"].filtered(
                lambda prod: prod.public_categ_ids.filtered(
                    lambda categ: categ.id in permitted_category_ids
                )
            )

            res.qcontext.update(
                {
                    "search_product": filtered_search_products,
                    "products": filtered_products,
                }
            )

            ppg = res.qcontext.get("ppg", 20)
            ppr = res.qcontext.get("ppr", 4)
            res.qcontext.update(
                {"bins": TableCompute().process(filtered_products, ppg, ppr)}
            )

        return request.render("website_sale.products", res.qcontext)
