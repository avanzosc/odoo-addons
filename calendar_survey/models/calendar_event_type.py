# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class CalendarEventType(models.Model):
    _inherit = 'calendar.event.type'

    survey_ids = fields.Many2many(comodel_name='survey.survey')
