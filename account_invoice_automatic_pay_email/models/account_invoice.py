# -*- coding: utf-8 -*-
# Copyright 2018 Gotzon Imaz - AvanzOSC
# Copyright 2018 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, api, fields
from dateutil.relativedelta import relativedelta


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    payment_reminder_date = fields.Date(
        string='Payment reminder date')

    @api.multi
    def automatic_pay_email(self):
        mail_template = self.env.ref(
            'account_invoice_automatic_pay_email.email_customers_payment_'
            'reminder', False)
        invoice_obj = self.env['account.invoice']
        if mail_template:
            cond = [('payment_reminder_date', '<=',
                     fields.Date.context_today(self)),
                    ('state', '=', 'open'),
                    ('type', '=', 'out_invoice'),
                    ('payment_term', '!=', False)]
            invoices = invoice_obj.search(cond)
            for invoice in invoices:
                if (invoice.payment_term.line_ids and
                        invoice.payment_term.line_ids[0].days > 0):
                    partners = invoice.partners_for_send_automatic_pay_email()
                    for partner in partners:
                        invoice.send_automatic_pay_email(
                            mail_template, partner)
                    today = fields.Date.context_today(self)
                    invoice.payment_reminder_date = fields.Date.to_string(
                        fields.Date.from_string(today) +
                        relativedelta(days=7))

    def partners_for_send_automatic_pay_email(self):
        return self.partner_id.ids

    def send_automatic_pay_email(self, mail_template, partner):
        mail = self.env['mail.compose.message'].with_context(
            default_composition_mode='mass_mail',
            default_template_id=mail_template.id,
            default_use_template=True,
            default_partner_ids=[(6, 0, [partner])],
            active_id=self.id,
            active_ids=self.ids,
            active_model='account.invoice',
            default_model='account.invoice',
            default_res_id=self.id,
            force_send=True
        ).create({'subject': mail_template.subject,
                  'body': mail_template.body_html})
        mail.send_mail()

    @api.multi
    def onchange_payment_term_date_invoice(self, payment_term_id,
                                           date_invoice):
        result = super(
            AccountInvoice, self).onchange_payment_term_date_invoice(
            payment_term_id, date_invoice)
        if result.get('value', False).get('date_due', False):
            result['value']['payment_reminder_date'] = (
                result.get('value').get('date_due'))
        return result
