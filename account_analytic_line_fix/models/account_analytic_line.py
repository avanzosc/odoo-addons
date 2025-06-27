# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("account_id", False):
                project_id = self._get_project_from_analytic_account(
                    vals.get("account_id")
                )
                if project_id:
                    vals["project_id"] = project_id
        lines = super().create(vals_list)
        return lines

    def write(self, values):
        if (
            "project_id" in values
            and values.get("project_id", False)
            and "product_uom_id" not in values
        ):
            return super(
                AccountAnalyticLine, self.with_context(project_without_product_uom=True)
            ).write(values)
        if values.get("account_id", False):
            project_id = self._get_project_from_analytic_account(
                values.get("account_id")
            )
            if project_id:
                values["project_id"] = project_id
        return super().write(values)

    def _get_project_from_analytic_account(self, analytic_account_id):
        analytic_account = self.env["account.analytic.account"].browse(
            analytic_account_id
        )
        if analytic_account and analytic_account.project_ids:
            return analytic_account.project_ids[0].id
        return False

    def _timesheet_preprocess(self, vals):
        if "project_without_product_uom" in self.env.context:
            vals["product_uom_id"] = self.product_uom_id.id
        return super()._timesheet_preprocess(vals)

    def _timesheet_postprocess_values(self, values):
        if "project_without_product_uom" in self.env.context:
            return {id_: {} for id_ in self.ids}
        return super()._timesheet_postprocess_values(values)
