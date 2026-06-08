# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class TreasuryForecast(models.Model):
    _inherit = "treasury.forecast"

    @api.depends("financing_id", "financing_id.project_id")
    def _compute_project_id(self):
        for forecast in self:
            if forecast.financing_id and forecast.financing_id.project_id:
                forecast.project_id = forecast.financing_id.project_id.id
            else:
                forecast.project_id = False

    @api.depends("financing_id", "financing_id.analytic_account_id")
    def _compute_analytic_account_id(self):
        for forecast in self:
            if forecast.financing_id and forecast.financing_id.analytic_account_id:
                forecast.analytic_account_id = (
                    forecast.financing_id.analytic_account_id.id
                )
            else:
                forecast.analytic_account_id = False

    project_id = fields.Many2one(
        comodel_name="project.project",
        string="Project",
        compute="_compute_project_id",
        store=True,
        readonly=False,
    )
    analytic_account_id = fields.Many2one(
        comodel_name="account.analytic.account",
        string="Analytic Account",
        compute="_compute_analytic_account_id",
        store=True,
        readonly=False,
    )

    @api.onchange("project_id")
    def _onchange_project_id(self):
        if self.project_id and self.project_id.account_id:
            self.analytic_account_id = self.project_id.account_id.id
        else:
            self.analytic_account_id = self.env.context.get(
                "default_analytic_account_id", False
            )
