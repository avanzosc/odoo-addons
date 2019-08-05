# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    amount_type = fields.Selection(
        selection=[('cost', 'Cost'),
                   ('revenue', 'Revenue')],
        compute='_compute_amount_type', string='Cost/Revenue', store=True)

    @api.depends('amount')
    def _compute_amount_type(self):
        for line in self:
            line.amount_type = 'cost' if line.amount < 0 else 'revenue'
