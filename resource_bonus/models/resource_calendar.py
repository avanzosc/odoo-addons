# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResourceCalendar(models.Model):
    _inherit = 'resource.calendar'

    bonus_ids = fields.One2many(
        comodel_name='resource.calendar.bonus', inverse_name='calendar_id',
        string='Bonuses')
