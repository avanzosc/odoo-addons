from datetime import datetime

from dateutil.relativedelta import relativedelta

from odoo import http
from odoo.http import request


class SaleOrderController(http.Controller):

    @http.route("/confirm_sale_order", type="http", auth="user", website=True)
    def confirm_sale_order(self, **kwargs):
        order_id = kwargs.get("order_id")
        if order_id:
            sale_order = request.env["sale.order"].sudo().browse(int(order_id))
            # Only change the order state if the partner_id of the order is the user,
            # for security reasons
            if (
                sale_order
                and sale_order.partner_id.id == request.env.user.partner_id.id
            ):
                sale_order.state = "sent"

                return request.redirect("/shop/cart")

        return request.redirect("/shop")

    @http.route("/draft_sale_order", type="http", auth="user", website=True)
    def draft_sale_order(self, **kwargs):
        order_id = kwargs.get("order_id")
        if order_id:
            sale_order = request.env["sale.order"].sudo().browse(int(order_id))
            # Only change the order state if the partner_id of the order is the user,
            # for security reasons
            if (
                sale_order
                and sale_order.partner_id.id == request.env.user.partner_id.id
            ):
                sale_order.state = "draft"

                current_website = request.website
                if current_website:
                    sale_order.website_id = current_website.id

                    abandoned_delay = sale_order.website_id.cart_abandoned_delay or 1.0
                    abandoned_datetime = datetime.utcnow() - relativedelta(
                        hours=abandoned_delay
                    )
                    sale_order.date_order = abandoned_datetime

                    return request.redirect("/shop/cart")

        return request.redirect("/shop")
