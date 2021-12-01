# Copyright 2021 Berezi - Iker - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api
import calendar


class EventRegistration(models.Model):
    _inherit = 'event.registration'

    student_id = fields.Many2one(
        string='Student', comodel_name='res.partner')
    education_center_id = fields.Many2one(
        string='Education center', related='student_id.education_center_id',
        comodel_name='res.partner', store=True)
    customer_id = fields.Many2one(
        string='Customer', related='event_id.customer_id', store=True)
    real_date_start = fields.Date(string='Real date start')
    date_start = fields.Date(
        string='Date start', help='Invoicing start date.')
    real_date_end = fields.Date(string='Real date end')
    date_end = fields.Date(
        string='Date end', help='Invoicing start end.')
    parent_email = fields.Char(
        string='Parent email', related='partner_id.email', store=True)
    student_email = fields.Char(
        string='Student email', related='student_id.email', store=True)

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        return

    @api.onchange("student_id", "partner_id")
    def _onchange_student_id(self):
        if self.student_id:
            self.name = self.student_id.name
            self.email = (self.student_id.email if self.student_id.email else
                          self.partner_id.email)
            self.phone = (self.student_id.phone if self.student_id.phone else
                          self.partner_id.phone)
            self.mobile = (self.student_id.mobile if self.student_id.mobile
                           else self.partner_id.mobile)
        if not self.student_id and self.partner_id:
            if not self.name:
                self.name = self.partner_id.name
            if not self.email:
                self.email = self.partner_id.email
            if not self.phone:
                self.phone = self.partner_id.phone
            if not self.mobile:
                self.mobile = self.partner_id.mobile

    @api.onchange('real_date_start')
    def _onchange_real_date_start(self):
        for registration in self:
            date_start = registration.real_date_start
            registration.date_start = (
                date_start if not date_start else date_start.replace(day=1))

    @api.onchange('real_date_end')
    def _onchange_real_date_end(self):
        for registration in self:
            date_end = registration.real_date_end
            if date_end:
                last_month_day = calendar.monthrange(
                    date_end.year, date_end.month)[1]
                date_end = date_end.replace(day=last_month_day)
            registration.date_end = date_end

    def action_confirm(self):
        super(EventRegistration, self).action_confirm()
        for registration in self:
            event_begin = registration.event_id.date_begin.date()
            today = fields.Date.context_today(self)
            if not registration.real_date_start:
                registration.real_date_start = (
                    event_begin if today < event_begin else today)
                registration._onchange_real_date_start()

    def action_cancel(self):
        super(EventRegistration, self).action_cancel()
        self._update_real_date_end()
        self.cancel_registration_contract()

    def action_set_done(self):
        super(EventRegistration, self).action_set_done()
        self._update_real_date_end()
        self.cancel_registration_contract()

    def action_set_draft(self):
        super(EventRegistration, self).action_set_draft()
        self.write({'real_date_start': None,
                    'real_date_end': None})
        self._onchange_real_date_start()
        self._onchange_real_date_end()

    def _update_real_date_end(self):
        for registration in self.filtered(lambda x: not x.real_date_end):
            event_end = registration.event_id.date_end.date()
            today = fields.Date.context_today(self)
            registration.real_date_end = (
                event_end if today > event_end else today)
            registration._onchange_real_date_end()

    def write(self, vals):
        result = super(EventRegistration, self).write(vals)
        if 'no_update_contract_line_dates' not in self.env.context:
            if (('date_start' in vals and vals.get('date_start', False)) or
                    ('date_end' in vals and vals.get('date_end', False))):
                registrations = self.filtered(
                    lambda x: x.sale_order_line_id and x.contract_line_id)
                if registrations:
                    registrations.update_dates_in_contract_line(vals)
        return result

    def update_dates_in_contract_line(self, vals):
        for registration in self:
            contract_line = registration.contract_line_id
            cond = [('contract_line_id', '=', contract_line.id)]
            registration = self.env['event.registration'].search(cond)
            if (registration and len(registration) == 1 and
                    contract_line.contract_id.invoice_count == 0):
                vals2 = {}
                if 'date_start' in vals and vals.get('date_start', False):
                    vals2['date_start'] = vals.get('date_start')
                if 'date_end' in vals and vals.get('date_end', False):
                    vals2['date_end'] = vals.get('date_end')
                contract_line.with_context(
                        no_update_event_reg_dates=True).write(vals2)

    def cancel_registration_contract(self):
        for registration in self.filtered(lambda x: x.contract_line_id):
            vals = {'contract_line_id': registration.contract_line_id.id,
                    'date_end': registration.date_end}
            wizard = self.env['contract.line.wizard'].create(vals)
            wizard.with_context(finish_from_registration=True).stop()
