# Copyright 2021 Berezi - Iker - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    event_id = fields.Many2one(
        string='Event', comodel_name='event.event',
        related='event_track_id.event_id', store=True)
    event_track_id = fields.Many2one(
        string='Event track', comodel_name='event.track')

    @api.onchange("event_track_id")
    def _onchange_event_track_id(self):
        for line in self:
            line.event_id = line.event_track_id.event_id

    @api.depends('task_id', 'task_id.project_id', 'event_id',
                 'event_id.project_id')
    def _compute_project_id(self):
        result = super(AccountAnalyticLine, self)._compute_project_id()
        for line in self.filtered(lambda line: line.event_id):
            if line.event_id.project_id:
                line.project_id = line.event_id.project_id.id
        return result
