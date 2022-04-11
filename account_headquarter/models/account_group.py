# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api


class AccountGroup(models.Model):
    _inherit = 'account.group'

    length_account = fields.Integer(
        string='Length account', compute='_compute_length_account',
        store=True)
    without_headquarter = fields.Boolean(
        string='Without headquarter in invoices and accounting entries',
        default=True)

    @api.depends('code_prefix_start')
    def _compute_length_account(self):
        for group in self:
            group.length_account = len(group.code_prefix_start)

    def _find_account_group_headquarter(self):
        found = False
        group = self
        while not found:
            if not group.parent_id:
                found = True
                without_headquarter_control = group.without_headquarter
            else:
                cond = [('id', '=', group.parent_id.id)]
                group = self.env['account.group'].search(cond, limit=1)
        return without_headquarter_control
