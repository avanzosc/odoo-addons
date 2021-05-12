# Copyright 2021 Berezi - Iker - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class EventTrack(models.Model):
    _inherit = 'event.track'

    analytic_account_id = fields.Many2one(
        string='Analytic account', comodel_name='account.analytic.account',
        related='event_id.analytic_account_id', store=True)
    account_analytic_line_ids = fields.One2many(
        string='Analytic lines', comodel_name='account.analytic.line',
        inverse_name='event_track_id')

    def _catch_values_for_create_analytic_line(self):
        name = u'{} {} {}'.format(
            self.event_id.name, self.name, self.date)
        analytic_line_vals = {
            'date': self.date,
            'unit_amount': self.duration,
            'name': name,
            'user_id': self.user_id.id,
            'account_id': self.analytic_account_id.id,
            'event_id': self.event_id.id,
            'event_track_id': self.id}
        return analytic_line_vals

    def _create_analytic_line(self):
        values = self._catch_values_for_create_analytic_line()
        self.env['account.analytic.line'].create(values)

    def write(self, vals):
        res = super(EventTrack, self).write(vals)
        if vals.get('stage_id'):
            stage = self.env['event.track.stage'].browse(vals['stage_id'])
            if stage.is_done:
                for track in self:
                    track._create_analytic_line()
        return res
