# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class AccountMove(models.Model):
    _inherit = 'account.move'

    headquarter_id = fields.Many2one(
        string='Headquarter', comodel_name='res.partner',
        domain="[('headquarter','=', True)]")

    def write(self, values):
        result = super(AccountMove, self).write(values)
        if 'headquarter_id' in values:
            for account_move in self:
                account_move.update_analytic_lines_hearquarter()
        return result

    def action_post(self):
        result = super(AccountMove, self).action_post()
        for account_move in self:
            account_move.update_analytic_lines_hearquarter()
        return result

    def update_analytic_lines_hearquarter(self):
        for invoice in self:
            for line in invoice.invoice_line_ids:
                if line.analytic_line_ids:
                    vals = {'headquarter_id': (invoice.headquarter_id.id
                                               if invoice.headquarter_id else
                                               False)}
                    line.analytic_line_ids.write(vals)
