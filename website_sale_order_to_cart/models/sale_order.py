from datetime import datetime
from odoo import models
from dateutil.relativedelta import relativedelta


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm_cart(self):
        for order in self:
            order.state = "sent"

    def action_charge_cart(self):
        for order in self:
            order.state = "draft"
            
            if not order.website_id:
                website = self.env["website"].sudo().search([], order="id asc", limit=1)
                order.website_id = website.id if website else False

            if not order.date_order:
                abandoned_delay = order.website_id.cart_abandoned_delay or 1.0
                abandoned_datetime = datetime.utcnow() - relativedelta(
                    hours=abandoned_delay
                )
                order.date_order = abandoned_datetime

        if order.website_id:
            base_url = order.website_id.get_base_url()
            cart_url = base_url.rstrip("/") + "/shop/cart"

            return {"type": "ir.actions.act_url", "url": cart_url, "target": "new"}
    
        return {"type": "ir.actions.act_url", "url": "/", "target": "self"}
