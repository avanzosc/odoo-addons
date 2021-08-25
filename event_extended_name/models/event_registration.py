# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class EventRegistration(models.Model):
    _inherit = 'event.registration'

    extended_name = fields.Char(
        string='Extended name', related='event_id.extended_name', store=True)
