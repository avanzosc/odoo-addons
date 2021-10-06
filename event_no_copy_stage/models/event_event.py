# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class EventEvent(models.Model):
    _inherit = 'event.event'

    stage_id = fields.Many2one(copy=False)
