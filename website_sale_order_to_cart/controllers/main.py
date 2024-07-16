from odoo import http
from odoo.http import request


class SaleOrderController(http.Controller):

    @http.route("/action_quotation_mark_send", type="http", auth="user", website=True)
    def action_quotation_mark_send(self, **kwargs):
        order_id = kwargs.get("order_id")
        if order_id:
            sale_order = request.env["sale.order"].sudo().browse(int(order_id))
            # Only change the order state if the partner_id of the order is the user
            if sale_order and sale_order.partner_id == request.env.user.partner_id:

                sale_order.action_quotation_mark_send()
                access_token = sale_order.access_token

                url = "/my/orders/{}?access_token={}".format(
                    sale_order.id, access_token
                )

                return request.redirect(url)

        return request.redirect("/shop")

    @http.route("/sale_order_to_cart", type="http", auth="user", website=True)
    def sale_order_to_cart(self, **kwargs):
        order_id = kwargs.get("order_id")
        if order_id:
            sale_order = request.env["sale.order"].sudo().browse(int(order_id))
            # Only change the order state if the partner_id of the order is the user
            if sale_order and sale_order.partner_id == request.env.user.partner_id:
                sale_order.sale_order_to_cart()
                return request.redirect("/shop/cart")

        return request.redirect("/shop")
