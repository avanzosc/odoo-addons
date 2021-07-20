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
        string='Date start', related='contract_line_id.date_start', store=True,
        help='Invoicing start date.')
    real_date_end = fields.Date(string='Real date end')
    date_end = fields.Date(
        string='Date end', related='contract_line_id.date_end', store=True,
        help='Invoicing start end.')
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
            self.name = self.partner_id.name
            self.email = self.partner_id.email
            self.phone = self.partner_id.phone
            self.mobile = self.partner_id.mobile

    @api.onchange('real_date_start')
    def _onchange_real_date_start(self):
        for registration in self.filtered(lambda x: x.real_date_start):
            real_date_start = registration.real_date_start
            if (registration.real_date_start <
                    registration.event_id.date_begin.date()):
                real_date_start = registration.event_id.date_begin.date()
            if not registration.date_start:
                registration.date_start = real_date_start.replace(day=1)

    @api.onchange('real_date_end')
    def _onchange_real_date_end(self):
        for registration in self.filtered(lambda x: x.real_date_end):
            if not registration.date_end:
                real_date_end = registration.real_date_end
                if (registration.real_date_end >
                        registration.event_id.date_end.date()):
                    real_date_end = registration.event_id.date_end.date()
                last_month_day = calendar.monthrange(
                    real_date_end.year, real_date_end.month)[1]
                date_end = real_date_end.replace(day=last_month_day)
                registration.date_end = date_end

    def action_confirm(self):
        super(EventRegistration, self).action_confirm()
        for registration in self:
            vals = {}
            real_date_start = fields.Date.context_today(self)
            if (fields.Date.context_today(self) <
                    registration.event_id.date_begin.date()):
                real_date_start = registration.event_id.date_begin.date()
            if not registration.real_date_start:
                vals['real_date_start'] = real_date_start
            if not registration.date_start:
                vals['date_start'] = real_date_start.replace(day=1)
            if vals:
                registration.write(vals)

    def action_cancel(self):
        super(EventRegistration, self).action_cancel()
        for registration in self:
            registration._update_end_dates()

    def action_set_done(self):
        super(EventRegistration, self).action_set_done()
        for registration in self:
            registration._update_end_dates()

    def action_set_draft(self):
        super(EventRegistration, self).action_set_draft()
        self.write({
            'real_date_start': None,
            'date_start': None,
            'real_date_end': None,
            'date_end': None
        })

    def _update_end_dates(self):
        real_date_end = fields.Date.context_today(self)
        if (fields.Date.context_today(self) > self.event_id.date_end.date()):
            real_date_end = self.event_id.date_end.date()
        last_month_day = calendar.monthrange(
            real_date_end.year, real_date_end.month)[1]
        date_end = real_date_end.replace(day=last_month_day)
        vals = {}
        if not self.real_date_end:
            vals['real_date_end'] = real_date_end
        if not self.date_end:
            vals['date_end'] = date_end
        if vals:
            self.write(vals)
