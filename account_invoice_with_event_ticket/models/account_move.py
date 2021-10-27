# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.depends('invoice_line_ids', 'invoice_line_ids.event_id',
                 'invoice_line_ids.event_ticket_id')
    def _compute_event_ticket_ids(self):
        for invoice in self:
            events = self.env['event.event']
            event_tickets = self.env['event.event.ticket']
            for line in invoice.invoice_line_ids:
                if line.event_id and line.event_id not in events:
                    events += line.event_id
                if (line.event_ticket_id and
                        line.event_ticket_id not in event_tickets):
                    event_tickets += line.event_ticket_id
            invoice.count_event = len(events)
            invoice.event_ids = [(6, 0, events.ids)]
            invoice.event_id = events[0].id if len(events) == 1 else False
            invoice.count_event_ticket = len(event_tickets)
            invoice.event_ticket_ids = [(6, 0, event_tickets.ids)]
            invoice.event_ticket_id = (
                event_tickets[0].id if len(event_tickets) == 1 else False)

    event_ids = fields.Many2many(
        string='Events', comodel_name='event.event',
        relation='rel_invoice_event', column1='account_move_id',
        column2='event_id', compute='_compute_event_ticket_ids', store=True,
        copy=False)
    event_ticket_ids = fields.Many2many(
        string='Event tickets', comodel_name='event.event.ticket',
        relation='rel_invoice_event_ticket', column1='account_move_id',
        column2='event_ticket_id', compute='_compute_event_ticket_ids',
        store=True, copy=False)
    count_event = fields.Integer(
        string='Num. events', compute='_compute_event_ticket_ids', copy=False,
        store=True)
    event_id = fields.Many2one(
        string='Event', comodel_name='event.event', copy=False, store=True,
        compute='_compute_count_event')
    count_event_ticket = fields.Integer(
        string='Num. event tickets', compute='_compute_event_ticket_ids',
        copy=False, store=True)
    event_ticket_id = fields.Many2one(
        string='Event ticket', comodel_name='event.event.ticket', copy=False,
        store=True, compute='_compute_count_event_ticket')
