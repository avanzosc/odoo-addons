# Copyright 2021 Berezi - Iker - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    event_id = fields.Many2one(
        string='Event', comodel_name='event.event')
    event_track_id = fields.Many2one(
        string='Event track', comodel_name='event.track')
    project_id = fields.Many2one(
        string='Project', related='event_id.project_id', store=True)

    @api.onchange("event_track_id")
    def _onchange_event_track_id(self):
        for line in self:
            line.event_id = line.event_track_id.event_id
