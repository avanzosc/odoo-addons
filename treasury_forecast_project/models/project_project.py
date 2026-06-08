# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models
from odoo.osv import expression
from odoo.tools.safe_eval import safe_eval


class ProjectProject(models.Model):
    _inherit = "project.project"

    def _compute_project_forecast_count(self):
        for project in self:
            cond = [("project_id", "=", project.id)]
            lines = self.env["treasury.forecast.project.report"].search(cond)
            project.project_forecast_count = len(lines)

    def _compute_treasury_financing_count(self):
        for project in self:
            cond = [("project_id", "=", project.id)]
            lines = self.env["treasury.financing"].search(cond)
            project.treasury_financing_count = len(lines)

    def _compute_treasury_forecast_count(self):
        for project in self:
            cond = [("project_id", "=", project.id)]
            lines = self.env["treasury.forecast"].search(cond)
            project.treasury_forecast_count = len(lines)

    project_forecast_count = fields.Integer(
        string="# Project Forecast", compute="_compute_project_forecast_count"
    )
    treasury_financing_count = fields.Integer(
        string="# Treasury Financing", compute="_compute_treasury_financing_count"
    )
    treasury_forecast_count = fields.Integer(
        string="# Treasury Forecast", compute="_compute_treasury_forecast_count"
    )

    def action_view_forecast_project(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id(
            "treasury_forecast_project.action_treasury_forecast_project_report_pivot"
        )
        action["domain"] = expression.AND(
            [
                [("project_id", "in", self.ids)],
                safe_eval(action.get("domain") or "[]"),
            ]
        )
        return action

    def action_view_treasury_financing(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id(
            "treasury_forecast.action_treasury_financing"
        )
        action["domain"] = expression.AND(
            [
                [("project_id", "in", self.ids)],
                safe_eval(action.get("domain") or "[]"),
            ]
        )
        context = safe_eval(action.get("context") or "{}")
        context.update(
            {
                "default_project_id": self.id,
            }
        )
        action.update(
            {
                "context": context,
            }
        )
        return action

    def action_view_treasury_forecast(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id(
            "treasury_forecast.action_treasury_forecast"
        )
        action["domain"] = expression.AND(
            [
                [("project_id", "in", self.ids)],
                safe_eval(action.get("domain") or "[]"),
            ]
        )
        context = safe_eval(action.get("context") or "{}")
        context.update(
            {
                "default_project_id": self.id,
            }
        )
        action.update(
            {
                "context": context,
            }
        )
        return action
