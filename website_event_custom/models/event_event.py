# Copyright 2021 Berezi - Iker - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api, _


class EventEvent(models.Model):
    _inherit = 'event.event'

    @api.depends('resource_calendar_id',
                 'resource_calendar_id.attendance_ids',
                 'resource_calendar_id.attendance_ids.dayofweek')
    def _compute_days(self):
        for event in self:
            my_text = ''
            my_days = event.resource_calendar_id.attendance_ids.mapped(
                'dayofweek')
            for my_day in my_days:
                actual_day = ''
                if my_day == '0':
                    actual_day = _('Monday')
                if my_day == '1':
                    actual_day = _('Tuesday')
                if my_day == '2':
                    actual_day = _('Wednesday')
                if my_day == '3':
                    actual_day = _('Thursday')
                if my_day == '4':
                    actual_day = _('Friday')
                if my_day == '5':
                    actual_day = _('Saturday')
                if my_day == '6':
                    actual_day = _('Sunday')
                if actual_day not in my_text:
                    if not my_text:
                        my_text = actual_day
                    else:
                        my_text = '{}, {}'.format(my_text, actual_day)
            event.days = my_text

    first_teacher_id = fields.Many2one(
        string='First Teacher', comodel_name='res.users')
    second_teacher_id = fields.Many2one(
        string='Second Teacher', comodel_name='res.users')
    resource_calendar_id= fields.Many2one(
        string='Event Schedule', comodel_name='resource.calendar')
    days = fields.Char(
        string='Days', compute='_compute_days', store=True)
