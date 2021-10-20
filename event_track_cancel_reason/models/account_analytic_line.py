# Copyright 2021 Berezi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    time_type_id = fields.Many2one(
        string='Time Type', comodel_name='project.time.type',
        related='event_track_id.time_type_id', store=True)
