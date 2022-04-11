# Copyright 2021 Berezi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class EventEvent(models.Model):
    _inherit = 'event.event'

    customer_service_id = fields.Many2one(
        string='Customer Service', comodel_name='resource.calendar')
    hours_advance = fields.Integer(string='Hours Advance', default=8)
