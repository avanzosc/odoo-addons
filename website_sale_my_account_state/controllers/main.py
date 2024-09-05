from odoo.http import request

from odoo.addons.portal.controllers.portal import pager as portal_pager
from odoo.addons.sale.controllers.portal import CustomerPortal


class CustomSalePortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        partner = request.env.user.partner_id

        SaleOrder = request.env["sale.order"]
        if "quotation_count" in counters:
            if SaleOrder.check_access_rights("read", raise_exception=False):
                values["quotation_count"] = SaleOrder.search_count(
                    self._prepare_quotations_domain(partner)
                )
            else:
                values["quotation_count"] = 0

        if "order_count" in counters:
            if SaleOrder.check_access_rights("read", raise_exception=False):
                values["order_count"] = SaleOrder.search_count(
                    self._prepare_orders_domain(partner)
                )
            else:
                values["order_count"] = 0

        return values

    def _prepare_quotations_domain(self, partner):
        domain = [
            ("message_partner_ids", "child_of", [partner.commercial_partner_id.id]),
            ("state", "in", ["sent", "cancel", "draft"]),
        ]
        return domain

    def _prepare_orders_domain(self, partner):
        domain = [
            ("message_partner_ids", "child_of", [partner.commercial_partner_id.id]),
            ("state", "in", ["sale"]),
        ]
        return domain

    def _prepare_sale_portal_rendering_values(
        self,
        page=1,
        date_begin=None,
        date_end=None,
        sortby=None,
        quotation_page=False,
        **kwargs
    ):
        values = super()._prepare_sale_portal_rendering_values(
            page=page,
            date_begin=date_begin,
            date_end=date_end,
            sortby=sortby,
            quotation_page=quotation_page,
            **kwargs
        )

        SaleOrder = request.env["sale.order"]

        partner_id = request.env.user.partner_id.id

        if quotation_page:
            domain = [
                ("partner_id", "=", partner_id),
                ("state", "in", ["draft", "sent", "cancel"]),
            ]
        else:
            domain = [("partner_id", "=", partner_id), ("state", "in", ["sale"])]

        if date_begin and date_end:
            domain += [
                ("create_date", ">", date_begin),
                ("create_date", "<=", date_end),
            ]

        searchbar_sortings = self._get_sale_searchbar_sortings()

        sort_order = searchbar_sortings.get(sortby, {"order": "date_order desc"}).get(
            "order"
        )

        pager_values = portal_pager(
            url=values.get("default_url"),
            total=SaleOrder.search_count(domain),
            page=page,
            step=self._items_per_page,
            url_args={"date_begin": date_begin, "date_end": date_end, "sortby": sortby},
        )

        orders = SaleOrder.search(
            domain,
            order=sort_order,
            limit=self._items_per_page,
            offset=pager_values["offset"],
        )

        values.update(
            {
                "quotations": orders.sudo() if quotation_page else SaleOrder,
                "orders": orders.sudo() if not quotation_page else SaleOrder,
                "pager": pager_values,
            }
        )

        return values
