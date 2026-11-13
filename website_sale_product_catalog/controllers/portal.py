# Copyright 2026 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from odoo import _, http
from odoo.http import request

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
            "all": {"label": _("All"), "domain": [("is_pubished", "=", True)]},
            "prebook": {
                "label": _("Prebook"),
                "domain": [
                    ("is_published", "=", True),
                    ("catalog_type_id.is_prebook", "=", True),
                ],
            },
        }
        return searchbar_filters

    def _prepare_catalog_portal_rendering_values(
        self,
        page=1,
        date_begin=None,
        date_end=None,
        sortby=None,
        groupby=None,
        quotation_page=False,
        **kwargs,
    ):
        Catalog = request.env["product.catalog"]

        if not sortby:
            sortby = "sequence"

        # default group by value
        if not groupby:
            groupby = "none"

        searchbar_filters = self._get_catalog_searchbar_filters()
        searchbar_groupby = self._get_catalog_searchbar_groupby()
        searchbar_sortings = self._get_catalog_searchbar_sortings()

        # partner = request.env.user.partner_id
        values = self._prepare_portal_layout_values()
        _items_per_page = 15

        url = "/my/catalogs"
        domain = Catalog._catalog_get_portal_domain()

        sort_order = searchbar_sortings[sortby]["order"]

        if date_begin and date_end:
            domain += [
                ("create_date", ">", date_begin),
                ("create_date", "<=", date_end),
            ]

        url_args = {"date_begin": date_begin, "date_end": date_end}

        if len(searchbar_sortings) > 1:
            url_args["sortby"] = sortby

        pager_values = portal_pager(
            url=url,
            total=Catalog.search_count(domain) if Catalog.has_access("read") else 0,
            page=page,
            step=_items_per_page,
            url_args=url_args,
        )
        catalogs = (
            Catalog.search(
                domain,
                order=sort_order,
                limit=_items_per_page,
                offset=pager_values["offset"],
            )
            if Catalog.has_access("read")
            else Catalog
        )

        values.update(
            {
                "date": date_begin,
                "catalogs": catalogs.sudo(),
                "page_name": "catalog",
                "pager": pager_values,
                "default_url": url,
                "searchbar_filters": searchbar_filters,
                "searchbar_groupby": searchbar_groupby,
                # 'searchbar_inputs': searchbar_inputs,
                # 'search_in': search_in,
                # 'search': search,
                "groupby": groupby,
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
