# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _update_event_registration_contract_line(self):
        result = super(
            SaleOrderLine, self)._update_event_registration_contract_line()
        for line in self:
            cond = [('contract_line_id', '=', line.contract_line_id.id)]
            registration = self.env['event.registration'].search(cond)
            if registration and len(registration) == 1:
                vals = {}
                if registration.date_start:
                    vals['date_start'] = registration.date_start
                if registration.date_end:
                    vals['date_end'] = registration.date_end
                if vals:
                    registration.contract_line_id.with_context(
                        no_update_event_reg_dates=True).write(vals)
        return result
