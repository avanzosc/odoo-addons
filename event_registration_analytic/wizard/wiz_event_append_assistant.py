# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models, api, exceptions, _
from datetime import datetime
import calendar


class WizEventAppendAssistant(models.TransientModel):
    _inherit = 'wiz.event.append.assistant'

    show_create_account = fields.Boolean(
        'Show create account', default=False)
    create_account = fields.Selection(
        [('yes', 'Yes'),
         ('no', 'No')], string='Create Account')

    @api.onchange('partner')
    def onchange_partner(self):
        self.show_create_account = False
        if self.partner:
            self.show_create_account = True
            event = self.env['event.event'].browse(
                self.env.context.get('active_id'))
            if not event.project_id:
                raise exceptions.Warning(
                    _('You must define a project in event'))
            if not event.project_id.analytic_account_id:
                raise exceptions.Warning(
                    _('The project defined in the event, not associated to an '
                      'analytical account'))
            if self.partner.employee:
                self.show_create_account = False

    @api.multi
    def action_append(self):
        self.ensure_one()
        event_obj = self.env['event.event']
        if self.show_create_account and not self.create_account:
            raise exceptions.Warning(
                _('You must enter if you want to create account for partner '
                  'registration'))
        result = super(WizEventAppendAssistant, self).action_append()
        if self.create_account:
            for event in event_obj.browse(self.env.context.get('active_ids')):
                registration = event.registration_ids.filtered(
                    lambda x: x.partner_id.id == self.partner.id and not
                    x.analytic_account)
                if registration:
                    self._create_account_for_employee_from_wizard(
                        event, registration)
        return result

    def _create_account_for_employee_from_wizard(self, event, registration):
        account_obj = self.env['account.analytic.account']
        analytic_invoice_line_obj = self.env['account.analytic.invoice.line']
        today = datetime.strptime(
            fields.Date.context_today(self), '%Y-%m-%d').date()
        recurrring_next_date = "%s-%s-%s" % (
            today.year, today.month,
            calendar.monthrange(today.year, today.month)[1])
        code = self.env['ir.sequence'].get(
            'account.analytic.account')
        vals = {'name': (_('Registration partner %s, event: %s') %
                         (registration.partner_id.name,
                          event.name)),
                'type': 'contract',
                'date_start': registration.date_start,
                'date': registration.date_end,
                'parent_id': event.project_id.analytic_account_id.id,
                'code': code,
                'partner_id': registration.partner_id.id,
                'recurring_invoices': True,
                'recurring_next_date': recurrring_next_date}
        new_account = account_obj.create(vals)
        registration.analytic_account = new_account.id
        for ticket in event.event_ticket_ids:
            line_vals = {'analytic_account_id': new_account.id,
                         'name': (ticket.sale_line.name or
                                  ticket.product_id.name),
                         'price_unit': ticket.price,
                         'price_subtotal': ticket.sale_line.price_subtotal,
                         'product_id': ticket.product_id.id,
                         'quantity': ticket.sale_line.product_uom_qty,
                         'uom_id': (ticket.sale_line.product_uom.id or
                                    ticket.product_id.uom_id.id)}
            analytic_invoice_line_obj.create(line_vals)
