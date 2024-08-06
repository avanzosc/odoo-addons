from datetime import datetime

from dateutil.relativedelta import relativedelta

from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_quotation_mark_send(self):
        self.state = "sent"
        self.user_id = self.partner_id.user_id

    def sale_order_to_cart(self):
        self.state = "draft"
        current_website = self.env["website"].get_current_website()
        if current_website:
            self.website_id = current_website.id

            abandoned_delay = current_website.cart_abandoned_delay or 1.0
            abandoned_datetime = datetime.utcnow() - relativedelta(
                hours=abandoned_delay
            )
            self.date_order = abandoned_datetime
