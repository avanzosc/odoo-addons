
from odoo import models


class EventRegistration(models.Model):
    _inherit = 'event.registration'

    def action_confirm(self):
        super(EventRegistration, self).action_confirm()
        if self.partner_id:

            if not self.event_ticket_id:
                self.select_ticket()

            if self.event_ticket_id:
                order = self.sale_order_id
                if not order:
                    order_obj = self.env['sale.order']
                    order = order_obj.search([
                        ('partner_id', '=', self.partner_id.id),
                        ('state', 'in', ('draft', 'sent'))
                    ], order='date_order desc', limit=1)
                    if not order:
                        order = order_obj.sudo().create({
                            'partner_id': self.partner_id.id
                        })
                    self.write({'sale_order_id': order.id})
                if not self.sale_order_line_id:
                    ticket_line = self.sale_order_id.order_line.filtered(
                        lambda l: l.product_id.id ==
                                  self.event_ticket_id.product_id.id)
                    order_line = None
                    if not ticket_line:
                        order_line = self.env['sale.order.line'].sudo().create(
                            {
                            'product_id': self.event_ticket_id.product_id.id,
                            'name': self.event_ticket_id.name,
                            'order_id': self.sale_order_id.id,
                            'product_uom':
                                self.event_ticket_id.product_id.uom_id.id})
                    else:
                        for line in ticket_line:
                            if line.product_id.id == \
                                    self.event_ticket_id.product_id.id:
                                order_line = line
                                break

                    self.write({'sale_order_line_id': order_line.id})
                    order._calculate_order_line_qty()

    def select_ticket(self):
        select_ticket = None
        available_tickets = self.event_id.event_ticket_ids
        if len(available_tickets) == 1:
            select_ticket = available_tickets
        elif len(available_tickets) > 1:
            member_ticket = available_tickets.filtered(
                    lambda t: t.is_member)
            if self.is_member:
                select_ticket = member_ticket
            elif member_ticket and len(available_tickets) == 2:
                select_ticket = available_tickets.filtered(
                    lambda t: not t.is_member)
        if select_ticket:
            self.write({'event_ticket_id': select_ticket.id})
