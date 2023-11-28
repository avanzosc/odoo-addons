# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        route_drop_shipping = self.env.ref(
            "stock_dropshipping.route_drop_shipping")
        result = super(SaleOrder, self).action_confirm()
        for sale in self:
            sale_lines = sale.order_line.filtered(
                lambda x: x.product_id)
            for sale_line in sale_lines:
                if route_drop_shipping in sale_line.product_id.route_ids:
                    sale_line.check_sequence_notes_in_purchase()
        return result
