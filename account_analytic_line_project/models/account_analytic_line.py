# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    project_info_id = fields.Many2one(
        string="Project Info",
        comodel_name="project.project",
        compute="_compute_project_info_id",
        store=True,
        readonly=False,
        copy=False,
    )
    project_type_id = fields.Many2one(
        string="Project Type",
        comodel_name="project.type",
        related="project_info_id.type_id",
        store=True,
        copy=False,
    )
    project_manager_id = fields.Many2one(
        string="Project Manager",
        comodel_name="res.users",
        related="project_info_id.user_id",
        store=True,
        copy=False,
    )
    allow_billable = fields.Boolean(
        related="project_info_id.allow_billable",
        store=True,
        copy=False,
    )

    @api.depends("project_id", "account_id")
    def _compute_project_info_id(self):
        for line in self:
            project_info_id = self.env["project.project"]
            if line.project_id:
                project_info_id = line.project_id.id
            if not line.project_id and line.account_id and line.account_id.project_ids:
                project_info_id = line.account_id.project_ids[0].id
            line.project_info_id = project_info_id
