# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class TreasuryForecast(models.Model):
    _inherit = "treasury.forecast"

    project_id = fields.Many2one(
        comodel_name="project.project", string="Project", compute=False
    )
    project_partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Partner Project",
        related="project_id.partner_id",
        store=True,
        readonly=True,
    )
    margin = fields.Float(string="Margin (%)")
    analytic_account_id = fields.Many2one(
        comodel_name="account.analytic.account",
        string="Analytic Account",
        compute=False,
    )

    @api.model
    def default_get(self, fields_list):
        values = super().default_get(fields_list)
        project_id = values.get("project_id") or self.env.context.get(
            "default_project_id"
        )
        if project_id and "margin" in fields_list:
            values["margin"] = (
                self.env["project.project"].browse(project_id).target_margin
            )
        return values

    @api.onchange("project_id")
    def _onchange_project_id(self):
        if self.project_id and self.project_id.account_id:
            self.analytic_account_id = self.project_id.account_id.id
        else:
            self.analytic_account_id = self.env.context.get(
                "default_analytic_account_id", False
            )
        if self.project_id:
            self.margin = self.project_id.target_margin
            self._onchange_margin()

    @api.onchange("margin")
    def _onchange_margin(self):
        if self.project_id:
            self.income_price = self.expense_price * (1 + self.margin / 100)
            self._update_project_amounts()

    @api.onchange("category_id")
    def _onchange_category_id(self):
        if self.project_id:
            self._update_project_amounts()

    @api.onchange("product_id")
    def _onchange_product_id(self):
        result = super()._onchange_product_id()
        if self.project_id and self.product_id:
            self.expense_price = self.product_id.standard_price
            self._onchange_margin()
            self._onchange_quantity_expense_price()
            self._onchange_quantity_income_price()
        return result

    @api.onchange("quantity", "expense_price")
    def _onchange_quantity_expense_price(self):
        if not self.project_id:
            return super()._onchange_quantity_expense_price()
        self._onchange_margin()

    @api.onchange("quantity", "income_price")
    def _onchange_quantity_income_price(self):
        if not self.project_id:
            return super()._onchange_quantity_income_price()
        self._update_project_amounts()

    def _update_project_amounts(self):
        category_type = self.category_id.category_type
        expense = self.quantity * self.expense_price
        income = self.quantity * self.income_price
        if category_type == "income":
            self.expense = 0.0
            self.income = income
        elif category_type == "expense":
            self.expense = expense
            self.income = 0.0
        elif category_type == "both":
            self.expense = expense
            self.income = income
        else:
            # Preserve the existing project behavior when no category is set.
            self.expense = expense
            self.income = income

    @api.onchange("expense")
    def _onchange_expense(self):
        if not self.project_id:
            return super()._onchange_expense()

    @api.onchange("income")
    def _onchange_income(self):
        if not self.project_id:
            return super()._onchange_income()
