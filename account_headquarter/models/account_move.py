# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, _
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = 'account.move'

    headquarter_id = fields.Many2one(
        string='Headquarter', comodel_name='res.partner',
        domain="[('headquarter','=', True)]")

    def action_post(self):
        result = super(AccountMove, self).action_post()
        for account_move in self:
            if account_move.headquarter_id:
                lines = account_move.invoice_line_ids.filtered(
                        lambda x: x.account_id and not
                        x.exclude_from_invoice_tab)
                if lines:
                    lines2 = lines.filtered(lambda x: not x.headquarter_id)
                    if lines2:
                        raise UserError(
                            _('There are lines that need to define their '
                              'Headquarter.'))
                    lines2 = lines.filtered(
                        lambda x: x.headquarter_id and not
                        x.analytic_account_id)
                    if lines2:
                        raise UserError(
                            _('There are lines that need to define their '
                              'analytic account.'))
                lines = account_move.invoice_line_ids.filtered(
                        lambda x: x.headquarter_id)
                lines.update_analytic_lines_hearquarter()
        return result
