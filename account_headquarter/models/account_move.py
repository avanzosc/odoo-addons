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
                for line in lines:
                    account_group = line.account_id.group_id
                    without_headquarter_control = (
                        account_group._find_account_group_headquarter())
                    if (not without_headquarter_control and not
                            line.headquarter_id):
                        raise UserError(
                            _('The line with accounting account: {}, need to '
                              'define their Headquarter.').format(
                                  line.account_id.name))
                if lines:
                    lines2 = lines.filtered(
                        lambda x: x.headquarter_id and not
                        x.analytic_account_id)
                    for line in lines2:
                        raise UserError(
                            _('The line with accounting account: {}, need to '
                              'define their analytic account.').format(
                                  line.account_id.name))
                lines = account_move.invoice_line_ids.filtered(
                        lambda x: x.headquarter_id)
                lines.update_analytic_lines_hearquarter()
        return result
