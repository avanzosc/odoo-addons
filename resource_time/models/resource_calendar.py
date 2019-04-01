# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ResourceCalendar(models.Model):
    _inherit = 'resource.calendar'

    hour_gap = fields.Float(string='Hour Gap', compute='_compute_hour_gap')

    @api.depends('attendance_ids', 'attendance_ids.hour_gap')
    def _compute_hour_gap(self):
        today = fields.Date.context_today(self)
        for record in self:
            attendances = record.attendance_ids.filtered(
                lambda a: ((not a.date_from or
                            (a.date_from and a.date_from <= today)) and
                           (not a.date_to or
                            (a.date_to and a.date_to >= today))))
            record.hour_gap = sum(attendances.mapped('hour_gap'))


class ResourceCalendarAttendance(models.Model):
    _inherit = 'resource.calendar.attendance'

    hour_gap = fields.Float(
        string='Hour Gap', compute='_compute_hour_gap', store=True)

    @api.depends('hour_from', 'hour_to')
    def _compute_hour_gap(self):
        for record in self:
            record.hour_gap = record.hour_to - record.hour_from
