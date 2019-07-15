# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields


class PaymentLine(models.Model):
    _inherit = 'payment.line'

    invoice_id = fields.Many2one(
        string='Invoice', comodel_name='account.invoice',
        related='move_line_id.invoice', store=True)
    payment_order_type = fields.Selection(
        string='Payment order type', related='order_id.payment_order_type',
        store=True)
    ml_maturity_date = fields.Date(
        string='Due Date', related='move_line_id.date_maturity', store=True)
