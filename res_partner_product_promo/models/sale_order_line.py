from odoo import models

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def action_assign_product_partner(self):
        for line in self:
            line.order_id.partner_id.promo_product_id = line.product_id
