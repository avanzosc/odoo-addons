# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    sale_order_line_id = fields.Many2one(
        string='Sale order line', comodel_name='sale.order.line',
        related='contract_line_id.sale_order_line_id', store=True)
    event_id = fields.Many2one(
        string='Event', comodel_name='event.event',
        related='sale_order_line_id.event_id', store=True)
    event_ticket_id = fields.Many2one(
        string='Event ticket', comodel_name='event.event.ticket',
        related='sale_order_line_id.event_ticket_id', store=True)
    event_address_id = fields.Many2one(
        string='Event address', comodel_name='res.partner',
        related='event_id.address_id', store=True)
