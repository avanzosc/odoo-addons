# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    invoice_line_count = fields.Integer(
        string='# Invoice Lines', compute='_compute_invoice_line_count')

    @api.depends('invoice_line_ids')
    def _compute_invoice_line_count(self):
        for invoice in self:
            invoice.invoice_line_count = len(invoice.invoice_line_ids)

    @api.multi
    def button_open_invoice_lines(self):
        self.ensure_one()
        action = self.env.ref(
            'account_invoice_usability.action_account_invoice_line')
        action_dict = action.read()[0] if action else {}
        action_dict['context'] = safe_eval(
            action_dict.get('context', '{}'))
        action_dict['context'].update(
            {'search_default_invoice_id': self.id,
             'default_invoice_id': self.id})
        domain = expression.AND([
            [('invoice_id', '=', self.id)],
            safe_eval(action.domain or '[]')])
        action_dict.update({'domain': domain})
        return action_dict
