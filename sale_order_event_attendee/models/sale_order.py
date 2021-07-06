
from odoo import models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.onchange('order_line')
    def _calculate_order_line_qty(self):
        for line in self.order_line:
            if line.product_id.event_ok:
                line_count = self.env['event.registration'].search_count(
                    [('sale_order_line_id', '=', line._origin.id)]
                )
                line.product_uom_qty = line_count
