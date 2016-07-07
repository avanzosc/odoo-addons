# -*- coding: utf-8 -*-
# © 2016 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, api


class AccountReportPaymentPartnerWizard(models.TransientModel):

    """Will launch partner ledger report and pass required args"""

    _inherit = "partners.ledger.webkit"
    _name = "report.payment.partner.webkit"

    commercial_id = fields.Many2one(comodel_name="res.users",
                                    string="Commercial")
    payment_mode = fields.Many2one(comodel_name="payment.mode",
                                   string="Payment Mode")

    @api.multi
    def pre_print_report(self, data):
        data = super(AccountReportPaymentPartnerWizard, self).pre_print_report(
            data)
        vals = self.read(['commercial_id', 'payment_mode'])[0]
        data['form'].update(vals)
        return data

    @api.multi
    def _print_report(self, data):
        # we update form with display account value
        data = self.pre_print_report(data)
        return {'type': 'ir.actions.report.xml',
                'report_name': 'account.account_report_partner_payment_webkit',
                'datas': data}
