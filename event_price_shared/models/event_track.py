# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class EventTrack(models.Model):
    _inherit = 'event.track'

    task_id = fields.Many2one(related=False)
    shared_price_event = fields.Boolean(
        string='Shared price event', related='event_id.shared_price_event',
        store=True)

    def _catch_values_for_create_analytic_line(self, partner):
        values = super(
            EventTrack, self)._catch_values_for_create_analytic_line(
                partner)
        if not self.event_id.shared_price_event:
            if self.event_id.task_id:
                values['task_id'] = self.event_id.task_id.id
            return values
        date = self.date.date()
        registrations = self.event_id.registration_ids.filtered(
            lambda x: x.student_id and x.real_date_start and
            date >= x.real_date_start and
            (not x.real_date_end or
             (x.real_date_end and date <= x.real_date_end)))
        tasks = self.env['project.task']
        for registration in registrations.filtered(lambda x: x.task_id):
            if registration.task_id not in tasks:
                tasks += registration.task_id
        for task in tasks:
            task_registrations = registrations.filtered(
                lambda x: x.task_id == task)
            values['task_id'] = task.id
            amount = ((self.duration / len(registrations)) *
                      len(task_registrations))
            values['unit_amount'] = amount
            self.env['account.analytic.line'].create(values)
        return {}
