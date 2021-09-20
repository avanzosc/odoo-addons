# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class ContractLine(models.Model):
    _inherit = 'contract.line'

    def write(self, vals):
        result = super(ContractLine, self).write(vals)
        if 'no_update_event_reg_dates' not in self.env.context:
            if (('date_start' in vals and vals.get('date_start', False)) or
                    ('date_end' in vals and vals.get('date_end', False))):
                lines = self.filtered(
                    lambda x: x.sale_order_id and x.sale_order_line_id and
                    x.sale_order_line_id.event_id and
                    x.sale_order_line_id.event_ticket_id)
                if lines:
                    lines.update_dates_in_event_registration(vals)
        return result

    def update_dates_in_event_registration(self, vals):
        for line in self:
            cond = [('contract_line_id', '=', line.id)]
            registration = self.env['event.registration'].search(cond)
            if registration and len(registration) == 1:
                vals2 = {}
                if 'date_start' in vals and vals.get('date_start', False):
                    vals2['date_start'] = vals.get('date_start')
                if 'date_end' in vals and vals.get('date_end', False):
                    vals2['date_end'] = vals.get('date_end')
                registration.with_context(
                        no_update_contract_line_dates=True).write(vals2)
