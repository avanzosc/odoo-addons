# Copyright 2021 Berezi - Iker - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api
from babel.util import distinct


class EventEvent(models.Model):
    _inherit = 'event.event'

    customer_id = fields.Many2one(
        string='Customer', comodel_name='res.partner')

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
        string='Main Responsible', comodel_name='res.users', copy=False)
    second_responsible_id = fields.Many2one(
        string='Second Responsible', comodel_name='res.users', copy=False)
    resource_calendar_id = fields.Many2one(
        string='Event Schedule', comodel_name='resource.calendar')
    days = fields.Char(
        string='Days', compute='_compute_days', store=True)
    copy_main_responsible = fields.Boolean(
        string='Copy main responsible', default=False,
        help='Copy main responsible when duplicate event')
    copy_second_responsible = fields.Boolean(
        string='Copy second responsible', default=False,
        help='Copy second responsible when duplicate event')

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        self.ensure_one()
        default = dict(default or {})
        if self.copy_main_responsible and self.main_responsible_id:
            default['main_responsible_id'] = self.main_responsible_id.id
        if self.copy_second_responsible and self.second_responsible_id:
            default['second_responsible_id'] = self.second_responsible_id.id
        return super(EventEvent, self).copy(default)
