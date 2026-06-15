# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import http
from odoo.http import request


class ProductCatalogWeb(http.Controller):
    @http.route("/shop/catalog", type="http", auth="user", website=True)
    def product_catalog(self, search="", **post):
        domain = [("active", "=", True), ("visible_slider", "=", True)]
        if search:
            domain += [("name", "ilike", search)]
        catalogs = request.env["product.catalog.web"].search(domain)
        return request.render(
            "product_catalog_web.product_catalog",
            {"catalogs": catalogs, "search": search},
        )
