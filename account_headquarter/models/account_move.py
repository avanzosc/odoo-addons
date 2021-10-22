# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class AccountMove(models.Model):
    _inherit = 'account.move'

    headquarter_id = fields.Many2one(
        string='Headquarter', comodel_name='res.partner',
        domain="[('headquarter','=', True)]")

    def action_post(self):
        result = super(AccountMove, self).action_post()
        for account_move in self:
            account_move.invoice_line_ids.update_analytic_lines_hearquarter()
        return result
