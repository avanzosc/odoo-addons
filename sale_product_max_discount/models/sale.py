# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, api


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    state = fields.Selection(selection_add=[('validation', 'Validation')])

    @api.multi
    def test_max_discounts_exceed(self):
        self.ensure_one()
        return bool(self.order_line.filtered(lambda x: x.discount >
                                             x.product_id.max_discount))

    @api.multi
    def action_validation(self):
        self.state = 'validation'
        self.send_mail()

    @api.multi
    def send_mail(self):
        mail_obj = self.env['mail.mail']
        sale_manager_group = self.env.ref('base.group_sale_manager')
        email_to = ', '.join(sale_manager_group.mapped('users.login'))
        for sale in self:
            body_tmpl = ("Some lines in the order had exceeded the maximum "
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
    def get_line_details(self):
        self.ensure_one()
        body_msg = ''
        for line in self.order_line.filtered(lambda x: x.discount >
                                             x.product_id.max_discount):
            body_msg_tmpl = (
                "<small><strong>Product:"
                "</strong> [{}] {}, <strong>Quantity:</strong> {}, <strong>"
                "Unit price:</strong> {}, <strong>Discount:</strong> {}, "
                "<strong>Line Subtotal:</strong> {},<strong>Maximum discount "
                "in product:</strong> {}<br/></small>")
            body_msg += body_msg_tmpl.format(
                line.product_id.default_code, line.product_id.name,
                line.product_uom_qty, line.price_unit, line.discount,
                line.price_subtotal, line.product_id.max_discount)
        return body_msg
