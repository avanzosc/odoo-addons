from datetime import datetime
from odoo import models

class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm_cart(self):
        for order in self:
            order.state = "sent"

    def action_charge_cart(self):
        for order in self:
            order.state = "draft"
            if not order.website_id:
                order.website_id = 1

            if not order.date_order:
                order.date_order = datetime.now()

        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        cart_url = base_url.rstrip('/') + '/shop/cart'

        return {
            'type': 'ir.actions.act_url',
            'url': cart_url,
            'target': 'new'
        }
