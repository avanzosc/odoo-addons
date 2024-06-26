from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm_cart(self):
        for order in self:
            order.state = "sent"
