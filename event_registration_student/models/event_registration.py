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
        string='Customer', related='event_id.customer_id')
    real_date_start = fields.Date(string='Real date start')
    date_start = fields.Date(string='Date start')
    real_date_end = fields.Date(string='Real date end')
    date_end = fields.Date(string='Date end')

    @api.onchange("student_id", "partner_id")
    def _onchange_student_id(self):
        self.partner_id = (self.student_id.commercial_partner_id.id
                           if self.customer_id.id == self.company_id.id else
                           self.event_id.customer_id.id)
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

    def action_confirm(self):
        super(EventRegistration, self).action_confirm()
        self.write({
            'real_date_start': fields.Date.context_today(self),
            'date_start': fields.Date.context_today(self).replace(day=1)
        })

    def action_cancel(self):
        super(EventRegistration, self).action_cancel()
        last_month_day = calendar.monthrange(
            fields.Date.context_today(self).year,
            fields.Date.context_today(self).month)[1]
        date_end = fields.Date.context_today(self).replace(day=last_month_day)
        self.write({
            'real_date_end': fields.Date.context_today(self),
            'date_end': date_end
        })

    def action_set_done(self):
        super(EventRegistration, self).action_set_done()
        last_month_day = calendar.monthrange(
            fields.Date.context_today(self).year,
            fields.Date.context_today(self).month)[1]
        date_end = fields.Date.context_today(self).replace(day=last_month_day)
        self.write({
            'real_date_end': fields.Date.context_today(self),
            'date_end': date_end
        })

    def action_set_draft(self):
        super(EventRegistration, self).action_set_draft()
        self.write({
            'real_date_start': None,
            'date_start': None,
            'real_date_end': None,
            'date_end': None
        })
