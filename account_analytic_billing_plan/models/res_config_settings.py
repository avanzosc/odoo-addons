# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from ast import literal_eval
from odoo import api, fields, models


class AccountConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    def _default_billing_plan_journal_id(self):
        return (self.env['account.invoice'].default_get(['journal_id'])
                ['journal_id'])

    billing_plan_journal_id = fields.Many2one(
        comodel_name='account.journal', domain="[('type', '=', 'sale')]",
        string='Default Journal for Billing Plan Invoices',
        default=_default_billing_plan_journal_id)

    @api.model
    def get_values(self):
        res = super(AccountConfigSettings, self).get_values()
        get_param = self.env['ir.config_parameter'].sudo().get_param
        # the value of the parameter is a nonempty string
        journal_id = literal_eval(
            get_param('account_analytic_billing_plan.billing_plan_journal_id',
                      default='False'))
        if (journal_id and
                not self.env['account.journal'].sudo().browse(
                    journal_id).exists()):
            journal_id = False
        res.update(
            billing_plan_journal_id=journal_id,
        )
        return res

    @api.multi
    def set_values(self):
        super(AccountConfigSettings, self).set_values()
        set_param = self.env['ir.config_parameter'].sudo().set_param
        # we store the repr of the values, since the value of the parameter is
        # a required string
        set_param('account_analytic_billing_plan.billing_plan_journal_id',
                  repr(self.billing_plan_journal_id.id))
