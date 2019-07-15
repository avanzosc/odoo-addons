# -*- coding: utf-8 -*-
# © 2016 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, api


class AccountReportPaymentPartnerWizard(models.TransientModel):

    """Will launch partner ledger report and pass required args"""

    _inherit = "partners.ledger.webkit"
    _name = "wizard.payment.partner.webkit"

    commercial_id = fields.Many2one(comodel_name="res.users",
                                    string="Commercial")
    payment_mode_ids = fields.Many2many(comodel_name="payment.mode",
                                        column1="pay_partner_wiz",
                                        column2="payment_mode",
                                        relation="pay_partner_wiz_mode",
                                        string="Payment Mode")
    allow_unpaid = fields.Boolean(string="Allow Unpaid")
    receives_in_account = fields.Boolean(string="Receives in Account")

    @api.multi
    def pre_print_report(self, data):
        data = super(AccountReportPaymentPartnerWizard, self).pre_print_report(
            data)
        data['form'].update({'commercial_id': self.commercial_id.id,
                             'payment_mode_ids': self.payment_mode_ids.ids,
                             'allow_unpaid': self.allow_unpaid,
                             'receives_in_account': self.receives_in_account})
        return data

    @api.multi
    def _print_report(self, data):
        data = self.pre_print_report(data)
        return {'type': 'ir.actions.report.xml',
                'report_name': 'account.account_report_partner_payment_webkit',
                'datas': data}
