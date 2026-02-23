# Copyright 2026 Aner Arregi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class TreasuryForecast(models.Model):
    _name = "treasury.forecast"
    _description = "Treasury Forecast"
    _order = "date desc, id desc"

    name = fields.Char(string="Description", required=True, copy=True)
    date = fields.Date(required=True, default=fields.Date.context_today)
    active = fields.Boolean(default=True)
    partner_id = fields.Many2one(comodel_name="res.partner", string="Partner")
    product_id = fields.Many2one(comodel_name="product.product", required=True)
    journal_id = fields.Many2one(
        comodel_name="account.journal", domain="[('type', 'in', ('bank', 'cash'))]"
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        required=True,
        default=lambda self: self.env.company,
    )
    currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Currency",
        required=True,
        default=lambda self: self.env.company.currency_id,
    )
    expense = fields.Monetary(currency_field="currency_id", group_operator="sum")
    income = fields.Monetary(currency_field="currency_id", group_operator="sum")
    balance = fields.Monetary(
        string="Line Balance",
        compute="_compute_balance",
        store=True,
        currency_field="currency_id",
        group_operator="sum",
    )
    recurrence_months = fields.Integer(string="Recurrence (Months)", default=1)

    @api.depends("income", "expense")
    def _compute_balance(self):
        for record in self:
            record.balance = record.income - record.expense

    @api.onchange("product_id")
    def _onchange_product_id(self):
        if self.product_id:
            self.name = self.product_id.description or self.product_id.display_name

    @api.onchange("expense")
    def _onchange_expense(self):
        if self.expense > 0:
            self.income = 0

    @api.onchange("income")
    def _onchange_income(self):
        if self.income > 0:
            self.expense = 0

    @api.constrains("expense", "income")
    def _check_values(self):
        for record in self:
            if record.expense < 0 or record.income < 0:
                raise ValidationError(
                    _("Values for expense and income must be positive.")
                )

    @api.constrains("recurrence_months")
    def _check_recurrence(self):
        for record in self:
            if record.recurrence_months < 1:
                raise ValidationError(_("Recurrence must be at least 1 month."))

    def action_open_generate_lines_wizard(self):
        active_ids = self.env.context.get("active_ids", self.ids)
        action = self.env.ref(
            "treasury_forecast.action_treasury_forecast_generate_lines"
        ).read()[0]
        action["context"] = dict(
            self.env.context, active_ids=active_ids, active_model="treasury.forecast"
        )
        return action
