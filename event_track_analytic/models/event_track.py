# Copyright 2021 Berezi - Iker - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class EventTrack(models.Model):
    _inherit = 'event.track'

    project_id = fields.Many2one(
        string='Project', comodel_name='project.project',
        related='event_id.project_id', store=True)
    analytic_account_id = fields.Many2one(
        string='Analytic account', comodel_name='account.analytic.account',
        related='event_id.analytic_account_id', store=True)
    account_analytic_line_ids = fields.One2many(
        string='Analytic lines', comodel_name='account.analytic.line',
        inverse_name='event_track_id')
