# -*- coding: utf-8 -*-
# © 2016 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import fields, models


class CalendarEvent(models.Model):
    _inherit = 'calendar.event'

    project_id = fields.Many2one(
        comodel_name='project.project', string='Project')
