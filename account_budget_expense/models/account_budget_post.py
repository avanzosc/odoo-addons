# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class AccountBudgetPost(models.Model):
    _inherit = 'account.budget.post'

    expenses = fields.Boolean(
        string='Expenses Position', default=False, copy=False)

    @api.constrains('expenses')
    def _check_expenses(self):
        if len(self.search([('expenses', '=', True)])) > 1:
            raise ValidationError(
                _('There can only be one expenses position.'))
