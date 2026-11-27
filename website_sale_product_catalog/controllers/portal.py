# Copyright 2026 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from operator import itemgetter

from odoo import _, http
from odoo.http import request
from odoo.osv.expression import AND
from odoo.tools import groupby as groupbyelem

from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.addons.portal.controllers.portal import pager as portal_pager


class CustomerPortal(CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)

        Catalog = request.env["product.catalog"]
        if "catalog_count" in counters:
            domain = Catalog._catalog_get_portal_domain()
            values["catalog_count"] = (
                Catalog.search_count(domain) if Catalog.has_access("read") else 0
            )

        return values

    def _get_catalog_searchbar_inputs(self):
        values = {
            "name": {"input": "name", "label": _("Catalog Name"), "sequence": 10},
            "catalog_type_id": {
                "input": "catalog_type_id",
                "label": _("Catalog Type"),
                "sequence": 20,
            },
        }
        return values

    def _get_catalog_search_domain(self, search_in, search):
        if search_in == "catalog_type_id":
            catalog_type_ids = (
                request.env["product.catalog.type"]
                .sudo()
                .search([("name", "ilike", search)])
            )
            return [("catalog_type_id", "in", catalog_type_ids.ids)]
        elif search_in in self._get_catalog_searchbar_inputs():
            return [(search_in, "ilike", search)]
        else:
            return ["|", ("name", "ilike", search), ("id", "ilike", search)]

    def _get_catalog_searchbar_sortings(self):
        return {
            "sequence": {"label": _("Sequence"), "order": "sequence asc"},
            "name": {"label": _("Name"), "order": "name asc"},
        }

    def _get_catalog_searchbar_groupby(self):
        values = {
            "none": {"label": _("None"), "sequence": 10},
            "catalog_type_id": {"label": _("Type"), "sequence": 20},
        }
        return values

    def _get_catalog_searchbar_filters(self, project_domain=None, task_domain=None):
        searchbar_filters = {
            "all": {"label": _("All"), "domain": []},
            "prebook": {
                "label": _("Prebook"),
                "domain": [
                    ("catalog_type_id.is_prebook", "=", True),
                ],
            },
        }
        return searchbar_filters

    def _prepare_catalog_portal_rendering_values(
        self,
        page=1,
        sortby=None,
        filterby=None,
        search=None,
        search_in="all",
        groupby="none",
        **kw,
    ):
        Catalog = request.env["product.catalog"]
        domain = Catalog._catalog_get_portal_domain()
        Catalog_sudo = Catalog.sudo()

        values = self._prepare_portal_layout_values()
        _items_per_page = 15

        searchbar_sortings = self._get_catalog_searchbar_sortings()
        searchbar_filters = self._get_catalog_searchbar_filters()
        searchbar_groupby = self._get_catalog_searchbar_groupby()
        searchbar_inputs = self._get_catalog_searchbar_inputs()

        # default sort by value
        if not sortby:
            sortby = "sequence"

        # default group by value
        if not groupby:
            groupby = "none"

        # default filter by value
        if not filterby:
            filterby = "all"
        domain = AND([domain, searchbar_filters[filterby]["domain"]])

        if search and search_in:
            domain = AND([domain, self._get_catalog_search_domain(search_in, search)])

        catalog_count = Catalog_sudo.search_count(domain)

        pager = portal_pager(
            url="/my/catalogs",
            url_args={
                "sortby": sortby,
                "search_in": search_in,
                "search": search,
                "filterby": filterby,
                "groupby": groupby,
            },
            total=catalog_count,
            page=page,
            step=_items_per_page,
        )

        def get_catalogs():
            field = None if groupby == "none" else groupby
            orderby = f"{field}, {sortby}" if field else sortby
            catalogs = Catalog_sudo.search(
                domain, order=orderby, limit=_items_per_page, offset=pager["offset"]
            )

            if groupby != "none":
                grouped_catalogs = [
                    Catalog_sudo.concat(*g)
                    for k, g in groupbyelem(catalogs, itemgetter(groupby))
                ]
            else:
                grouped_catalogs = [catalogs] if catalogs else []
            return catalogs, grouped_catalogs

        catalogs, grouped_catalogs = get_catalogs()
        values.update(
            {
                "catalogs": catalogs,
                "grouped_catalogs": grouped_catalogs,
                "page_name": "catalog",
                "pager": pager,
                "default_url": "/my/catalogs",
                "search_in": search_in,
                "search": search,
                "groupby": groupby,
                "filterby": filterby,
                "searchbar_inputs": searchbar_inputs,
                "searchbar_groupby": searchbar_groupby,
                "searchbar_filters": searchbar_filters,
            }
        )

        if len(searchbar_sortings) > 1:
            values.update(
                {
                    "sortby": sortby,
                    "searchbar_sortings": searchbar_sortings,
                }
            )
        return values

    @http.route(
        ["/my/catalogs", "/my/catalogs/page/<int:page>"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_catalogs(self, **kwargs):
        values = self._prepare_catalog_portal_rendering_values(**kwargs)
        request.session["my_catalogs_history"] = values["catalogs"].ids[:100]
        return request.render("website_sale_product_catalog.portal_my_catalogs", values)
