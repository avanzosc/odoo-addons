# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields


class CrmClaim(models.Model):
    _inherit = 'crm.claim'

    event_id = fields.Many2one(
        string='Event', comodel_name='event.event')
    event_track_id = fields.Many2one(
        string='Event track', comodel_name='event.track')
