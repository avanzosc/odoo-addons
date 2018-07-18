# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields


class PaymentLine(models.Model):
    _inherit = 'payment.line'

    student = fields.Many2one(
        comodel_name='res.partner', string='Student',
        related='move_line_id.invoice.student', store=True)
    event_address_id = fields.Many2one(
        comodel_name='res.partner', string='Event address',
        related='move_line_id.invoice.event_address_id', store=True)
    event_id = fields.Many2one(
        comodel_name='event.event', string='Event',
        related='move_line_id.invoice.event_id', store=True)
    sale_order_id = fields.Many2one(
        comodel_name='sale.order', string='Sale order',
        related='move_line_id.invoice.sale_order_id', store=True)
