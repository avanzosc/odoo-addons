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
            if lines:
                lines._update_event_registration_contract_line()
        return result
