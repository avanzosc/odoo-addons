# Copyright 2021 Berezi - Iker - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    event_id = fields.Many2one(
        string='Event', comodel_name='event.event')
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

    @api.model
    def create(self, values):
        if 'event_track_id' in values and values.get('event_track_id', False):
            track = self.env['event.track'].browse(
                values.get('event_track_id'))
            values['event_id'] = track.event_id.id
        return super(AccountAnalyticLine, self).create(values)

    def write(self, vals):
        if 'event_track_id' in vals and vals.get('event_track_id', False):
            track = self.env['event.track'].browse(
                vals.get('event_track_id'))
            vals['event_id'] = track.event_id.id
        return super(AccountAnalyticLine, self).write(vals)
