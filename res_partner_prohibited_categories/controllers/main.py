from odoo import http
from odoo.http import request

from odoo.addons.website_sale.controllers.main import WebsiteSale


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

        all_prohibited_category_ids = set(
            partner.prohibited_category_ids.ids
            + partner.related_prohibited_category_ids.ids
        )

        filtered_categories = res.qcontext["categories"].filtered(
            lambda c: c.id not in all_prohibited_category_ids
        )

        res.qcontext.update(
            {
                "categories": filtered_categories,
            }
        )

        return request.render("website_sale.products", res.qcontext)
