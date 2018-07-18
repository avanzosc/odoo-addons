# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import _, api, fields, models
from openerp.addons.event_track_assistant._common import _convert_to_local_date
import calendar

str2date = fields.Date.from_string


class WizEventAppendAssistant(models.TransientModel):
    _inherit = 'wiz.event.append.assistant'

    create_account = fields.Boolean(
        string='Show create account', default=False)

    @api.onchange('partner')
    def onchange_partner(self):
        create_account = False
        if self.registration and self.partner:
            create_account = True
            sale_order = self.registration.event_id.sale_order
            if (self.partner.employee or self.registration.analytic_account or
                    sale_order.project_id.recurring_invoices):
                create_account = False
        self.create_account = create_account

    @api.multi
    def action_append(self):
        self.ensure_one()
        event_obj = self.env['event.event']
        result = super(WizEventAppendAssistant, self).action_append()
        if self.create_account and not self.registration:
            for event in event_obj.browse(self.env.context.get('active_ids')):
                registration = event.registration_ids.filtered(
                    lambda x: x.partner_id.id == self.partner.id and not
                    x.analytic_account)
                if registration:
                    self._create_account_for_not_employee_from_wizard(
                        event, registration)
        elif self.create_account and self.registration:
            self._create_account_for_not_employee_from_wizard(
                self.registration.event_id, self.registration)
        elif (not self.create_account and self.registration and
                self.registration.analytic_account):
            self.registration.analytic_account.write(
                self._prepare_data_for_account_not_employee(
                    self.registration.event_id, self.registration))
        if self.registration:
            self.registration.analytic_account.set_open()
        return result

    def _create_account_for_not_employee_from_wizard(
            self, event, registration):
        account_obj = self.env['account.analytic.account']
        analytic_invoice_line_obj = self.env['account.analytic.invoice.line']
        vals = self._prepare_data_for_account_not_employee(event, registration)
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

    def _prepare_data_for_account_not_employee(self, event, registration):
        tz = self.env.user.tz
        if self.from_date and self.to_date:
            from_date = self.from_date
            to_date = self.to_date
            today = str2date(self.from_date)
        else:
            from_date = _convert_to_local_date(registration.date_start,
                                               tz=tz).date()
            to_date = _convert_to_local_date(registration.date_end,
                                             tz=tz).date()
            today = str2date(fields.Datetime.now())
        recurring_next_date = "{}-{}-{}".format(
            today.year, today.month,
            calendar.monthrange(today.year, today.month)[1])
        code = self.env['ir.sequence'].get(
            'account.analytic.account')
        parent_id = event.project_id.analytic_account_id.id or False
        if len(event.my_task_ids) == 1:
            parent_id = event.my_task_ids[0].project_id.analytic_account_id.id
        vals = {'name': (_('Student: %s - Payer: %s') %
                         (registration.partner_id.name,
                          registration.partner_id.parent_id.name)),
                'type': 'contract',
                'date_start': from_date,
                'date': to_date,
                'parent_id': parent_id,
                'code': code,
                'partner_id': registration.partner_id.parent_id.id,
                'student': registration.partner_id.id,
                'recurring_invoices': True,
                'recurring_next_date': recurring_next_date}
        if (registration.analytic_account and
                registration.analytic_account.recurring_next_date):
            old = str2date(registration.analytic_account.recurring_next_date)
            new = str2date(recurring_next_date)
            if old > new:
                vals['recurring_next_date'] = old
        if registration.event_id.sale_order:
            vals['sale'] = registration.event_id.sale_order.id
        return vals
