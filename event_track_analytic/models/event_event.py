# Copyright 2021 Berezi - Iker - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api


class EventEvent(models.Model):
    _inherit = 'event.event'

    project_id = fields.Many2one(
        string='Project', comodel_name='project.project')
    analytic_account_id = fields.Many2one(
        string='Analytic account', comodel_name='account.analytic.account',
        related='project_id.analytic_account_id', store=True)
    account_analytic_line_ids = fields.One2many(
        string='Analytic lines', comodel_name='account.analytic.line',
        inverse_name='event_id')

    @api.model
    def create(self, values):
        event = super(EventEvent, self).create(values)
        event.project_id = event._create_event_project().id
        return event

    def _create_event_project(self):
        project_vals = self.values_for_create_project()
        return self.env['project.project'].create(project_vals)

    def values_for_create_project(self):
        project_vals = {
            'name': self.name}
        return project_vals

    @api.onchange("project_id")
    def _onchange_project_id(self):
        if 'no_update_project' not in self.env.context and self.project_id:
            self.with_context(
                no_update_name=True).name = self.project_id.name

    @api.onchange("name")
    def _onchange_name(self):
        if ('no_update_name' not in self.env.context and self.name and
                self.project_id):
            self.project_id.with_context(
                no_update_project=True).name = self.name
