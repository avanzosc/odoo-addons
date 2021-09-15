# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _action_confirm(self):
        result = super(SaleOrder, self)._action_confirm()
        for sale in self:
            lines = sale.order_line.filtered(
                lambda x: x.contract_line_id and x.event_id and
                x.event_ticket_id)
            for line in lines:
                cond = [('event_id', '=', line.event_id.id),
                        ('event_ticket_id', '=', line.event_ticket_id.id),
                        ('sale_order_line_id', '=', line.id),
                        ('contract_line_id', '=', False)]
                registration = self.env['event.registration'].search(cond)
                if registration and len(registration) == 1:
                    registration.contract_line_id = line.contract_line_id.id
        return result
