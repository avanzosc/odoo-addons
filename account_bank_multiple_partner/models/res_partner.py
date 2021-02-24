# Copyright 2021 Daniel Campos - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ResPartnerBank(models.Model):
    _inherit = 'res.partner.bank'

    is_shared = fields.Boolean(string='Is shared bank account',
                               help="Check this if is a shared bank account")

    _sql_constraints = [
        ('unique_number', 'Check(1=1)', 'Account Number must be unique'),
    ]

    @api.constrains('sanitized_acc_number', 'company_id', 'is_shared')
    def _check_bank_number(self):
        number = self.search(
            [('sanitized_acc_number', '=', self.sanitized_acc_number),
             ('company_id', '=', self.company_id.id),
             ('is_shared', '=', False)])
        if len(number) > 1:
            raise ValidationError(_('Account Number must be unique'))
