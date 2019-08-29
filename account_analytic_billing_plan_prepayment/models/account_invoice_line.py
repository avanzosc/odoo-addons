# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    prepayment_plan_id = fields.Many2one(
        comodel_name='account.analytic.billing.plan',
        string='Prepayment Billing Plan')
