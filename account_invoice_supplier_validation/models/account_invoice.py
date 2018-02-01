# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, fields, models
from openerp.tools import config


class AccountInvoice(models.Model):

    _inherit = 'account.invoice'

    state = fields.Selection(selection_add=[('validation', 'To Valid')])

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
        account_manager_group = self.env.ref('account.group_account_manager')
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
            values = {
                'subject': u'{}: Invoice needs review'.format(
                    invoice.supplier_invoice_number),
                'body': body,
                'body_html': body,
                'notification': True,
                'email_to': invoice.user_id.login,
                'model': 'account.invoice',
                'res_id': invoice.id,
            }
            mail = mail_obj.create(values)
            mail.send()
