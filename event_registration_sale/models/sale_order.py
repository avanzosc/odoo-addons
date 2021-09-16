# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _action_confirm(self):
        for sale in self:
            for line in sale.order_line.filtered(
                    lambda x: x.event_ticket_id):
                if line.product_id != line.event_ticket_id.product_id:
                    line.product_id = line.event_ticket_id.product_id.id
                    line.product_id_change()
                if line.price_unit != line.event_ticket_id.price:
                    line.price_unit = line.event_ticket_id.price
                    line._onchange_discount()
        return super(SaleOrder, self)._action_confirm()
