from odoo import fields, models


class TreasuryForecastReport(models.Model):
    _name = "treasury.forecast.report"
    _description = "Treasury Forecast Report"
    _auto = False

    date = fields.Date()
    partner_id = fields.Many2one("res.partner", string="Partner")
    product_id = fields.Many2one("product.product", string="Product")
    product_category_id = fields.Many2one(
        comodel_name="product.category",
        string="Product Category",
        readonly=True,
    )
    name = fields.Char(string="Description")

    journal_id = fields.Many2one("account.journal", string="Journal")
    estimated_journal_id = fields.Many2one(
        "account.journal",
        string="Estimated Journal",
    )
    currency_id = fields.Many2one("res.currency", string="Currency")

    debit = fields.Monetary(string="Income", currency_field="currency_id")
    credit = fields.Monetary(string="Expense", currency_field="currency_id")
    balance = fields.Monetary(currency_field="currency_id")
    residual = fields.Monetary(currency_field="currency_id")

    source = fields.Selection(
        [("forecast", "Forecast"), ("move_line", "Move Line")],
        string="Origin",
    )
    financing_id = fields.Many2one("treasury.financing", string="Financing")

    category_id = fields.Many2one("treasury.financing.category", string="Category")

    parent_category_id = fields.Many2one(
        "treasury.financing.category", string="Parent Category"
    )
