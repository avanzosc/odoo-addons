# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models
from odoo.osv import expression
from odoo.tools.safe_eval import safe_eval


class ProjectProject(models.Model):
    _inherit = "project.project"

    target_margin = fields.Integer(string="Target Margin (%)")
    treasury_margin_calculation = fields.Selection(
        selection=[
            ("cost", "Margin on Cost Price"),
            ("sale", "Margin on Sale Price"),
        ],
        default="cost",
        required=True,
        help=(
            "Choose how the sale price is calculated for this project.\n\n"
            "Margin on Cost Price:\n"
            "Sale Price = Cost Price * (1 + Margin / 100)\n"
            "Example: Cost 100, Margin 20% -> Sale Price 120.\n\n"
            "Margin on Sale Price:\n"
            "Sale Price = Cost Price / (1 - Margin / 100)\n"
            "Example: Cost 100, Margin 20% -> Sale Price 125.\n\n"
            "The default method is taken from the company settings, "
            "but it can be changed for each project."
        ),
    )

    @api.model
    def default_get(self, fields_list):
        values = super().default_get(fields_list)

        if "treasury_margin_calculation" in fields_list and not values.get(
            "treasury_margin_calculation"
        ):
            company_id = values.get("company_id") or self.env.company.id
            company = self.env["res.company"].browse(company_id)
            values["treasury_margin_calculation"] = (
                company.treasury_margin_calculation or "cost"
            )

        return values

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
        action["domain"] = [("project_id", "in", self.ids)]
        context = safe_eval(action.get("context") or "{}")
        context.update(
            {
                "default_project_id": self.id,
                "hide_project_analytic": False,
            }
        )
        action.update(
            {
                "context": context,
            }
        )
        return action

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if "treasury_margin_calculation" not in vals:
                company = (
                    self.env["res.company"].browse(vals["company_id"])
                    if vals.get("company_id")
                    else self.env.company
                )
                vals["treasury_margin_calculation"] = (
                    company.treasury_margin_calculation or "cost"
                )
        return super().create(vals_list)

    @api.onchange("company_id")
    def _onchange_company_treasury_margin_calculation(self):
        if not self._origin.id:
            company = self.company_id or self.env.company
            self.treasury_margin_calculation = (
                company.treasury_margin_calculation or "cost"
            )
