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
    payment_mode_id = fields.Many2one(comodel_name="payment.mode",
                                      string="Payment Mode")

    @api.multi
    def pre_print_report(self, data):
        data = super(AccountReportPaymentPartnerWizard, self).pre_print_report(
            data)
        data['form'].update({'commercial_id': self.commercial_id.id,
                             'payment_mode_id': self.payment_mode_id.id})
        return data

    @api.multi
    def _print_report(self, data):
        data = self.pre_print_report(data)
        return {'type': 'ir.actions.report.xml',
                'report_name': 'account.account_report_partner_payment_webkit',
                'datas': data}
