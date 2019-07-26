# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class AccountAnalyticBillingPlan(models.Model):
    _inherit = 'account.analytic.billing.plan'

    prepayment = fields.Boolean(
        compute='_compute_prepayment', compute_sudo=True)
    final_invoice = fields.Boolean()

    @api.depends('product_id')
    def _compute_prepayment(self):
        prepayment_type = self.env.ref('account.data_account_type_prepayments')
        for plan in self:
            accounts = plan.product_id.product_tmpl_id.get_product_accounts()
            plan.prepayment = (
                accounts.get('income').user_type_id == prepayment_type)
