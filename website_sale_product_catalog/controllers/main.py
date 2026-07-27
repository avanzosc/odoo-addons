# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import logging

import werkzeug.exceptions

from odoo import _, fields, http
from odoo.http import request
from odoo.osv import expression

from odoo.addons.website_sale.controllers.main import WebsiteSale

_logger = logging.getLogger(__name__)

CATALOG_ITEMS_PER_PAGE = 48
CATALOG_PRODUCTS_LAYOUT_SESSION_KEY = "website_sale_product_catalog_products_layout"
CATALOGS_LAYOUT_SESSION_KEY = "website_sale_product_catalog_catalogs_layout"


def _website_catalog_domain():
    return [
        ("active", "=", True),
        ("visible_slider", "=", True),
        ("company_id", "=", request.env.company.id),
    ]


def _parse_catalog_ids(params):
    raw = params.get("catalog_ids", "") or ""
    try:
        return [int(x) for x in raw.split(",") if x.strip()]
    except (ValueError, TypeError):
        return []


def _get_catalog_layout_mode(session_key, default="grid"):
    layout_mode = request.params.get("layout")
    if layout_mode in ("grid", "list"):
        request.session[session_key] = layout_mode
        return layout_mode
    return request.session.get(session_key) or default


def _item_product_tmpl(item):
    return item.product_id.product_tmpl_id if item.product_id else item.product_tmpl_id


def _item_attribute_values(item):
    if item.product_id:
        return item.product_id.product_template_attribute_value_ids.mapped(
            "product_attribute_value_id"
        )
    if item.product_tmpl_id:
        return item.product_tmpl_id.attribute_line_ids.mapped("value_ids")
    return item.env["product.attribute.value"]


def _get_catalog_attribute_map(items):
    attrib_map = {}
    for item in items:
        for value in _item_attribute_values(item):
            attribute = value.attribute_id
            if attribute.id not in attrib_map:
                attrib_map[attribute.id] = {"attr": attribute, "values": {}}
            attrib_map[attribute.id]["values"][value.id] = value
    return attrib_map


def _get_catalog_attributes(attrib_map):
    return [
        {
            "attr": v["attr"],
            "values": sorted(v["values"].values(), key=lambda x: x.name),
        }
        for v in sorted(attrib_map.values(), key=lambda x: x["attr"].name)
        if v["values"]
    ]


def _get_customer_catalog_items(catalog):
    """Return current customer-pricelist items for the catalog products."""
    product_ids = catalog.pricelist_item_ids.mapped("product_id").ids
    if not product_ids:
        return request.env["product.pricelist.item"]

    now = fields.Datetime.now()
    return (
        request.env["product.pricelist.item"]
        .sudo()
        .search(
            [
                ("pricelist_id", "=", request.website.pricelist_id.id),
                ("product_id", "in", product_ids),
                "|",
                ("date_start", "=", False),
                ("date_start", "<=", now),
                "|",
                ("date_end", "=", False),
                ("date_end", ">=", now),
            ]
        )
    )


def _item_matches(
    item,
    search,
    search_term,
    sel_categ_ids,
    filter_min,
    filter_max,
    attrib_groups,
    website,
):
    tmpl = _item_product_tmpl(item)
    if search:
        searchable_values = [tmpl.name]
        if item.product_id:
            searchable_values.append(
                item.product_id.with_context(display_default_code=False).display_name
            )
        if not any(search_term in (v or "").casefold() for v in searchable_values):
            return False
    public_categ_ids = tmpl.public_categ_ids.filtered(
        lambda categ: not categ.website_id or categ.website_id == website
    ).ids
    if sel_categ_ids and not set(public_categ_ids).intersection(sel_categ_ids):
        return False
    if filter_min is not None and item.fixed_price < filter_min:
        return False
    if filter_max is not None and item.fixed_price > filter_max:
        return False
    if attrib_groups:
        item_val_ids = set(_item_attribute_values(item).ids)
        if not item_val_ids:
            return False
        if not all(
            any(v in item_val_ids for v in vals) for vals in attrib_groups.values()
        ):
            return False
    return True


class WebsiteCatalog(http.Controller):
    @http.route("/catalogs", type="http", auth="public", website=True)
    def catalogs(self, search=None, **post):
        search = (search or "").strip()
        domain = _website_catalog_domain()
        if search:
            domain = expression.AND(
                [
                    domain,
                    expression.OR(
                        [
                            [("name", "ilike", search)],
                            [("description", "ilike", search)],
                        ]
                    ),
                ]
            )
        show_catalogs = not request.env.user._is_public()
        catalogs = (
            request.env["product.catalog"].sudo().search(domain)
            if show_catalogs
            else request.env["product.catalog"]
        )
        layout_mode = _get_catalog_layout_mode(CATALOGS_LAYOUT_SESSION_KEY)
        return request.render(
            "website_sale_product_catalog.catalogs",
            {
                "catalogs": catalogs,
                "show_catalogs": show_catalogs,
                "search": search,
                "layout_mode": layout_mode,
            },
        )

    @http.route(
        "/catalog/save_layout_mode",
        type="json",
        auth="public",
        website=True,
    )
    def save_layout_mode(self, page, layout_mode):
        assert layout_mode in ("grid", "list"), _("Invalid catalog layout mode")
        if page == "catalogs":
            request.session[CATALOGS_LAYOUT_SESSION_KEY] = layout_mode
        else:
            request.session[CATALOG_PRODUCTS_LAYOUT_SESSION_KEY] = layout_mode
        return True

    @http.route(
        ["/catalog/<int:catalog_id>", "/catalog/<int:catalog_id>/page/<int:page>"],
        type="http",
        auth="public",
        website=True,
    )
    def catalog_detail(
        self,
        catalog_id,
        page=1,
        min_price=None,
        max_price=None,
        search=None,
        order=None,
        **post,
    ):
        catalog = (
            request.env["product.catalog"]
            .sudo()
            .search(
                _website_catalog_domain() + [("id", "=", catalog_id)],
                limit=1,
            )
        )
        if not catalog:
            raise werkzeug.exceptions.NotFound()

        args = request.httprequest.args
        sel_categ_ids = [int(x) for x in args.getlist("categ_id") if x.isdigit()]
        sel_attrib_ids = [int(x) for x in args.getlist("attrib") if x.isdigit()]
        search = (search or "").strip()
        search_term = search.casefold()
        available_orders = {"name_asc", "name_desc", "price_asc", "price_desc"}
        order = order if order in available_orders else ""
        layout_mode = _get_catalog_layout_mode(CATALOG_PRODUCTS_LAYOUT_SESSION_KEY)

        all_items = _get_customer_catalog_items(catalog).filtered(
            lambda i: (
                i.product_id
                and i.product_id.active
                and i.product_id.product_tmpl_id.active
            )
            or (not i.product_id and i.product_tmpl_id and i.product_tmpl_id.active)
        )

        categ_map = {}

        for item in all_items:
            tmpl = _item_product_tmpl(item)
            public_categs = tmpl.public_categ_ids.filtered(
                lambda categ: not categ.website_id
                or categ.website_id == request.website
            )
            for categ in public_categs:
                categ_map[categ.id] = categ

        categs = sorted(categ_map.values(), key=lambda c: c.name)

        try:
            filter_min = float(min_price) if min_price else None
            filter_max = float(max_price) if max_price else None
        except (ValueError, TypeError):
            filter_min = filter_max = None

        website = request.website
        items_before_price = all_items.filtered(
            lambda item: _item_matches(
                item,
                search,
                search_term,
                sel_categ_ids,
                None,
                None,
                {},
                website,
            )
        )
        base_attrib_map = _get_catalog_attribute_map(items_before_price)

        attrib_groups = {}
        active_sel_attrib_ids = []
        for val_id in sel_attrib_ids:
            for aid, ainfo in base_attrib_map.items():
                if val_id in ainfo["values"]:
                    attrib_groups.setdefault(aid, []).append(val_id)
                    active_sel_attrib_ids.append(val_id)
                    break
        sel_attrib_ids = active_sel_attrib_ids

        items_before_price = (
            items_before_price.filtered(
                lambda item: _item_matches(
                    item,
                    search,
                    search_term,
                    sel_categ_ids,
                    None,
                    None,
                    attrib_groups,
                    website,
                )
            )
            if attrib_groups
            else items_before_price
        )

        price_vals = [
            item.fixed_price for item in items_before_price if item.fixed_price
        ]
        price_min_all = min(price_vals, default=0.0)
        price_max_all = max(price_vals, default=0.0)

        items = items_before_price.filtered(
            lambda item: _item_matches(
                item,
                search,
                search_term,
                sel_categ_ids,
                filter_min,
                filter_max,
                {},
                website,
            )
        )
        attrib_map = _get_catalog_attribute_map(items)
        for aid in attrib_groups:
            if aid in base_attrib_map:
                attrib_map[aid] = base_attrib_map[aid]
        attributes = _get_catalog_attributes(attrib_map)

        items = items.sorted(
            key=lambda item: (
                item.product_id.product_tmpl_id.website_sequence
                if item.product_id
                else item.product_tmpl_id.website_sequence,
                item.id,
            )
        )
        if order:
            reverse = order.endswith("_desc")
            if order.startswith("name_"):
                items = items.sorted(
                    key=lambda item: (item.product_id or item.product_tmpl_id)
                    .with_context(display_default_code=False)
                    .display_name.casefold(),
                    reverse=reverse,
                )
            else:
                items = items.sorted(
                    key=lambda item: item.fixed_price,
                    reverse=reverse,
                )

        items_count = len(items)
        url_args = request.httprequest.args.copy()
        url_args.pop("page", None)
        pager = request.website.pager(
            url=f"/catalog/{catalog.id}",
            total=items_count,
            page=page,
            step=CATALOG_ITEMS_PER_PAGE,
            scope=5,
            url_args=url_args,
        )
        offset = pager["offset"]
        paged_items = items[offset : offset + CATALOG_ITEMS_PER_PAGE]

        return request.render(
            "website_sale_product_catalog.catalog_detail",
            {
                "catalog": catalog,
                "items": paged_items,
                "items_count": items_count,
                "items_total": len(all_items),
                "pager": pager,
                "ppg": CATALOG_ITEMS_PER_PAGE,
                "categs": categs,
                "attributes": attributes,
                "price_min_all": price_min_all,
                "price_max_all": price_max_all,
                "filter_min": filter_min,
                "filter_max": filter_max,
                "search": search,
                "order": order,
                "layout_mode": layout_mode,
                "sel_categ_ids": sel_categ_ids,
                "sel_attrib_ids": sel_attrib_ids,
                "has_filters": bool(
                    sel_categ_ids
                    or sel_attrib_ids
                    or filter_min
                    or filter_max
                    or search
                ),
            },
        )


class WebsiteSaleCatalog(WebsiteSale):
    @http.route(
        ["/shop/cart/update"],
        type="http",
        auth="public",
        methods=["POST"],
        website=True,
    )
    def cart_update(self, product_id, add_qty=1, set_qty=0, **kwargs):
        result = super().cart_update(
            product_id=product_id, add_qty=add_qty, set_qty=set_qty, **kwargs
        )
        try:
            catalog_id = int(kwargs.get("catalog_id", 0))
        except (ValueError, TypeError):
            catalog_id = 0
        if catalog_id:
            return request.redirect(f"/catalog/{catalog_id}")
        return result

    def _prepare_product_values(self, product, category, search, **kwargs):
        values = super()._prepare_product_values(product, category, search, **kwargs)
        catalog_id = request.params.get("catalog_id")
        if catalog_id:
            try:
                catalog = (
                    request.env["product.catalog"]
                    .sudo()
                    .search(
                        _website_catalog_domain() + [("id", "=", int(catalog_id))],
                        limit=1,
                    )
                )
                if catalog:
                    values["catalog"] = catalog
            except (ValueError, TypeError):
                _logger.debug(
                    "Ignored invalid catalog_id=%r in product page URL.", catalog_id
                )
        return values

    def _get_shop_domain(
        self, search, category, attrib_values, search_in_description=True
    ):
        domain = super()._get_shop_domain(
            search, category, attrib_values, search_in_description
        )
        catalog_ids = _parse_catalog_ids(request.params)
        if catalog_ids:
            catalogs = (
                request.env["product.catalog"]
                .sudo()
                .search(_website_catalog_domain() + [("id", "in", catalog_ids)])
            )
            tmpl_ids = catalogs._get_product_tmpl_ids()
            domain = expression.AND([domain, [("id", "in", tmpl_ids)]])
        return domain

    def _shop_lookup_products(self, attrib_set, options, post, search, website):
        fuzzy_search_term, product_count, search_result = super()._shop_lookup_products(
            attrib_set, options, post, search, website
        )
        catalog_ids = _parse_catalog_ids(request.params)
        if catalog_ids:
            catalogs = (
                request.env["product.catalog"]
                .sudo()
                .search(_website_catalog_domain() + [("id", "in", catalog_ids)])
            )
            catalog_tmpl_ids = set(catalogs._get_product_tmpl_ids())
            search_result = search_result.filtered(lambda p: p.id in catalog_tmpl_ids)
            product_count = len(search_result)
        return fuzzy_search_term, product_count, search_result

    def _shop_get_query_url_kwargs(
        self,
        category,
        search,
        min_price,
        max_price,
        order=None,
        tags=None,
        attribute_value=None,
        **post,
    ):
        kwargs = super()._shop_get_query_url_kwargs(
            category,
            search,
            min_price,
            max_price,
            order=order,
            tags=tags,
            attribute_value=attribute_value,
            **post,
        )
        if post.get("catalog_ids"):
            kwargs["catalog_ids"] = post["catalog_ids"]
        return kwargs

    def _get_additional_extra_shop_values(self, values, **post):
        res = super()._get_additional_extra_shop_values(values, **post)
        catalogs = (
            request.env["product.catalog"].sudo().search(_website_catalog_domain())
        )
        res.update(
            {
                "shop_catalogs": catalogs,
                "selected_catalog_ids": _parse_catalog_ids(request.params),
            }
        )
        return res
