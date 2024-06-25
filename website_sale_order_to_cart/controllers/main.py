from odoo import http
from odoo.http import request

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
