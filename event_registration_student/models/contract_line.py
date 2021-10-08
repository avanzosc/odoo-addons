# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields
from dateutil.relativedelta import relativedelta


class ContractLine(models.Model):
    _inherit = 'contract.line'

    account_move_line_ids = fields.One2many(
        string='Invoice lines', comodel_name='account.move.line',
        inverse_name='contract_line_id')

    def write(self, vals):
        if len(self) == 1 and vals.get('date_end', False):
            try:
                date_end = vals.get('date_end') + relativedelta(days=-1)
            except Exception:
                date_end = (fields.Date.from_string(vals.get('date_end')) +
                            relativedelta(days=-1))
            if self.last_date_invoiced:
                vals['last_date_invoiced'] = date_end
            if ('recurring_next_date' in vals and not
                    vals.get('reccurring_next_date')):
                vals['recurring_next_date'] = vals.get('date_end')
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
