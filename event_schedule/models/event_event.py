# Copyright 2021 Berezi - Iker - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api
from babel.util import distinct


class EventEvent(models.Model):
    _inherit = 'event.event'

    @api.depends('resource_calendar_id',
                 'resource_calendar_id.attendance_ids',
                 'resource_calendar_id.attendance_ids.dayofweek')
    def _compute_days(self):
        for event in self:
            my_days = []
            for attendance in event.resource_calendar_id.attendance_ids:
                field = attendance._fields["dayofweek"]
                day = field.convert_to_export(
                    attendance["dayofweek"], attendance)
                my_days.append(day)
            event.days = ', '.join(distinct(my_days))

    main_responsible_id = fields.Many2one(
        string='Main Responsible', comodel_name='res.users')
    second_responsible_id = fields.Many2one(
        string='Second Responsible', comodel_name='res.users')
    resource_calendar_id = fields.Many2one(
        string='Event Schedule', comodel_name='resource.calendar')
    days = fields.Char(
        string='Days', compute='_compute_days', store=True)
