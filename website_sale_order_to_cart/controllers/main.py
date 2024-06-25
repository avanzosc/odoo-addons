from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo import http
from odoo.http import request
from odoo.addons.payment.controllers.post_processing import PaymentPostProcessing
from odoo.exceptions import AccessError, MissingError, ValidationError


class WebsiteSale(WebsiteSale):
    @http.route()
    def shop_payment_validate(self, sale_order_id=None, **post):
        """ Method that should be called by the server when receiving an update
        for a transaction. State at this point :

         - UDPATE ME
        """
        if sale_order_id is None:
            order = request.website.sale_get_order()
            if not order and 'sale_last_order_id' in request.session:
                # Retrieve the last known order from the session if the session key `sale_order_id`
                # was prematurely cleared. This is done to prevent the user from updating their cart
                # after payment in case they don't return from payment through this route.
                last_order_id = request.session['sale_last_order_id']
                order = request.env['sale.order'].sudo().browse(last_order_id).exists()
        else:
            order = request.env['sale.order'].sudo().browse(sale_order_id)
            assert order.id == request.session.get('sale_last_order_id')

        errors = self._get_shop_payment_errors(order)
        if errors:
            first_error = errors[0]  # only display first error
            error_msg = f"{first_error[0]}\n{first_error[1]}"
            raise ValidationError(error_msg)

        tx = order.get_portal_last_transaction() if order else order.env['payment.transaction']

        # if not order or (order.amount_total and not tx):
        if not order:
            return request.redirect('/shop')

        if order and not order.amount_total and not tx:
            order.with_context(send_email=True).action_confirm()
            return request.redirect(order.get_portal_url())

        # clean context and session, then redirect to the confirmation page
        request.website.sale_reset()
        if tx and tx.state == 'draft':
            return request.redirect('/shop')

        PaymentPostProcessing.remove_transactions(tx)
        return request.redirect('/shop/confirmation')

class SaleOrderController(http.Controller):

    @http.route('/confirm_sale_order', type='http', auth='user', website=True)
    def confirm_sale_order(self, **kwargs):
        order_id = kwargs.get('order_id')
        if order_id:
            sale_order = request.env['sale.order'].sudo().browse(int(order_id))
            if sale_order:
                sale_order.action_confirm()

                return request.redirect('/shop/cart')
        
        return request.redirect('/shop')
