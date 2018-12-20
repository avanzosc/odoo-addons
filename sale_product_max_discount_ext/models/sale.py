# -*- coding: utf-8 -*-
# Copyright 2018 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    def send_mail(self, emails=None):
        if not emails:
            permissions = self.company_id.sale_manager_validations.filtered(
                lambda x: x.notification)
            if not permissions:
                return super(SaleOrder, self).send_mail()
            emails = permissions.mapped('user_id.login')
        mail_obj = self.env['mail.mail']
        email_to = ', '.join(emails)
        for sale in self:
            body_tmpl = (u"Some lines in the order had exceeded the maximum "
                         "discount defined in the product.<br/><strong>Order "
                         "number:</strong> {}<br/><strong>Customer:</strong> "
                         "{}<br/><strong>Product Details:</strong><br/>{}")
            body = body_tmpl.format(sale.name, sale.partner_id.name,
                                    sale.get_line_details())
            values = {
                'subject': '{}: Maximum discount exceeded'.format(sale.name),
                'body': body,
                'body_html': body,
                'email_to': email_to,
            }
            mail = mail_obj.create(values)
            mail.send()

    @api.multi
    def test_user_permissions(self):
        self.ensure_one()
        permissions = self.company_id.sale_manager_validations.filtered(
            lambda x: x.user_id.id == self._uid)
        return permissions.validation
