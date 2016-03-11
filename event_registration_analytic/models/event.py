# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api, exceptions, _


class EventEvent(models.Model):
    _inherit = 'event.event'

    def _create_event_from_sale(self, by_task, sale, line=False):
        event = super(EventEvent, self)._create_event_from_sale(
            by_task, sale, line=line)
        if by_task:
            self._create_event_ticket(event, line)
        else:
            sale_lines = sale.order_line.filtered(
                lambda x: x.recurring_service)
            for line in sale_lines:
                self._create_event_ticket(event, line)
        return event

    def _create_event_ticket(self, event, line):
        ticket_obj = self.env['event.event.ticket']
        line.product_id.event_ok = True
        ticket_vals = {'event_id': event.id,
                       'product_id': line.product_id.id,
                       'name': line.name,
                       'price': line.price_subtotal,
                       'sale_line': line.id}
        ticket = ticket_obj.create(ticket_vals)
        line.write({'event_id': event.id,
                    'event_ticket_id': ticket.id,
                    'event_ok': True})


class EventRegistration(models.Model):
    _inherit = 'event.registration'

    analytic_account = fields.Many2one(
        'account.analytic.account', string='Analytic account')
    is_employee = fields.Boolean(string='Is employee', default=False)

    @api.onchange('partner_id', 'partner_id.employee')
    def _onchange_partner(self):
        self.is_employee = False
        if self.partner_id and self.partner_id.employee:
            self.is_employee = True

    @api.multi
    def registration_open(self):
        wiz_obj = self.env['wiz.event.append.assistant']
        result = super(EventRegistration, self).registration_open()
        event = self.env['event.event'].browse(
            result['context'].get('event_id'))
        if not event.project_id:
            raise exceptions.Warning(
                _('You must define a project in event'))
        if not event.project_id.analytic_account_id:
            raise exceptions.Warning(
                _('The project defined in the event, not associated to an '
                  'analytical account'))
        wiz = wiz_obj.browse(result.get('res_id'))
        wiz.show_create_account = True
        if self.partner_id.employee or self.analytic_account:
            wiz.show_create_account = False
        return result


class EventEventTicket(models.Model):
    _inherit = 'event.event.ticket'

    sale_line = fields.Many2one(
        'sale.order.line', string='Sale line')
