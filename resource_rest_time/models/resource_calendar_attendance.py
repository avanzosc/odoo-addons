# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResourceCalendarAttendance(models.Model):
    _inherit = 'resource.calendar.attendance'

    rest_time = fields.Float(string='Rest Time')
