# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class TreasuryForecast(models.Model):
    _inherit = "treasury.forecast"

    project_id = fields.Many2one(
        comodel_name="project.project", string="Project", compute=False
    )
    analytic_account_id = fields.Many2one(
        comodel_name="account.analytic.account",
        string="Analytic Account",
        compute=False,
    )

    @api.onchange("project_id")
    def _onchange_project_id(self):
        if self.project_id and self.project_id.account_id:
            self.analytic_account_id = self.project_id.account_id.id
        else:
            self.analytic_account_id = self.env.context.get(
                "default_analytic_account_id", False
            )
