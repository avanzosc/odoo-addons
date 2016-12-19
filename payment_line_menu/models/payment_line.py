# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields


class PaymentLine(models.Model):
    _inherit = 'payment.line'

    payment_order_type = fields.Selection(
        [('payment', 'Payment'), ('debit', 'Direct debit')], store=True,
        string='Payment order type', related='order_id.payment_order_type')
    ml_maturity_date = fields.Date(
        string='Due Date', related='move_line_id.date_maturity', store=True)
