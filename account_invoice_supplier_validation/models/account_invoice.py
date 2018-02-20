# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, fields, models
from openerp.tools import config
import re


class AccountInvoice(models.Model):

    _inherit = 'account.invoice'

    @api.multi
    def _compute_readonly_user(self):
        for record in self:
            record.readonly_user = bool(self.env.uid != record.user_id.id)

    state = fields.Selection(selection_add=[('validation', 'In Review')])
    readonly_user = fields.Boolean(string="Readonly User",
                                   compute="_compute_readonly_user")

    @api.multi
    def test_supplier_invoice(self):
        self.ensure_one()
        if (config['test_enable'] and
                self.name != 'Test supplier invoice validation'):
            return False
        if self.type in ('in_invoice', 'in_refund'):
            return True
        return False

    @api.multi
    def action_validation(self):
        self.state = 'validation'
        self.send_mail()

    @api.multi
    def send_mail(self):
        mail_obj = self.env['mail.mail']
        mail_patt = r"[^@]+@[^@]+\.[^@]+"
        for invoice in self:
            body_tmpl = (
                u"The invoice <strong>{}</strong>, needs to be reviewed.<br/>"
                "<br/><span class='oe_mail_footer_access'><small>Link to "
                "Invoice <a style='color:inherit' href='{}'>{}</a></small>"
                "</span><br/>")
            url = self.env['ir.config_parameter'].sudo().get_param(
                'web.base.url')
            complete_url = (u'{}/web#id={}&view_type=form&model='
                            'account.invoice'.format(url, invoice.id))
            body = body_tmpl.format(invoice.supplier_invoice_number,
                                    complete_url,
                                    invoice.supplier_invoice_number)
            email_to = invoice.user_id.login
            if not re.match(mail_patt, email_to) and \
                    invoice.user_id.partner_id.email and \
                    re.match(mail_patt, invoice.user_id.partner_id.email):
                email_to = invoice.user_id.partner_id.email
            values = {
                'subject': u'{}: Invoice needs review'.format(
                    invoice.supplier_invoice_number),
                'body': body,
                'body_html': body,
                'notification': True,
                'email_to': email_to,
                'model': 'account.invoice',
                'res_id': invoice.id,
            }
            mail = mail_obj.create(values)
            mail.send()

    @api.multi
    def onchange_partner_id(
            self, type, partner_id, date_invoice=False, payment_term=False,
            partner_bank_id=False, company_id=False):
        res = super(AccountInvoice, self).onchange_partner_id(
            type, partner_id, date_invoice=date_invoice,
            payment_term=payment_term, partner_bank_id=partner_bank_id,
            company_id=company_id)
        if type in ('in_invoice', 'in_refund'):
            partner = self.env['res.partner'].browse(partner_id)
            if partner.hr_department and \
                    partner.hr_department.manager_id.user_id:
                res.get('value', {}).update(
                    {'user_id': partner.hr_department.manager_id.user_id.id})
        return res
