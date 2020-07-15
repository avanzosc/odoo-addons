# Copyright 2020 Adrian Revilla - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, api


class SaleOrderReport(models.Model):
    _inherit = 'sale.order'

#     coas_report_1_signature = fields.Binary(
#         'Signature 1', help='Signature for All reports',
#         copy=False, attachment=True)
#     coas_report_2_signature = fields.Binary(
#         'Signature 2', help='Signature for Service contrating',
#         copy=False, attachment=True)
#     coas_report_3_signature = fields.Binary(
#         'Signature 3', help='Signature for Annual voluntary contribution',
#         copy=False, attachment=True)
#     coas_report_4_signature = fields.Binary(
#         'Signature 4', help='Signature for AMPA annual membership fee',
#         copy=False, attachment=True)
#     coas_report_5_signature = fields.Binary(
#         'Signature 5', help='Signature for Voluntary monthly contribution',
#         copy=False, attachment=True)
#     coas_report_6_signature = fields.Binary(
#         'Signature 6',
#         help='Signature for Application for continuation of studies insurance',
#         copy=False, attachment=True)
#     coas_report_7_signature = fields.Binary(
#         'Signature 7',
#         help='Signature for Authorization for medicine administration',
#         copy=False, attachment=True)
#     coas_report_8_signature = fields.Binary(
#         'Signature 8',
#         help='Signature for Authorization to maintain the students hygiene',
#         copy=False, attachment=True)
# 
#     coas_report_1_signed_by = fields.Char(
#         'Signed by 1',
#         help='Name of the person that signed All reports.',
#         copy=False)
#     coas_report_2_signed_by = fields.Char(
#         'Signed by 2',
#         help='Name of the person that signed Service contrating.',
#         copy=False)
#     coas_report_3_signed_by = fields.Char(
#         'Signed by 3',
#         help='Name of the person that signed Annual voluntary contribution.',
#         copy=False)
#     coas_report_4_signed_by = fields.Char(
#         'Signed by 4',
#         help='Name of the person that signed AMPA annual membership fee.',
#         copy=False)
#     coas_report_5_signed_by = fields.Char(
#         'Signed by 5',
#         help='Name of the person that signed Voluntary monthly contribution.',
#         copy=False)
#     coas_report_6_signed_by = fields.Char(
#         'Signed by 6',
#         help='Name of the person that signed Application for continuation of studies insurance.',
#         copy=False)
#     coas_report_7_signed_by = fields.Char(
#         'Signed by 7',
#         help='Name of the person that signed Authorization for medicine administration.',
#         copy=False)
#     coas_report_8_signed_by = fields.Char(
#         'Signed by 8',
#         help='Name of the person that signed Authorization to maintain the students hygiene.',
#         copy=False)

    @api.multi
    def action_print_reports(self):
        return self.env.ref(
            'custom_v12_reports.sale_order_full_report').report_action(self)


class AccountBankingMandateReport(models.Model):
    _inherit = 'account.banking.mandate'

    @api.multi
    def action_print_reports(self):
        return self.env.ref(
            'custom_v12_reports.account_banking_mandate_report').report_action(
                self)
