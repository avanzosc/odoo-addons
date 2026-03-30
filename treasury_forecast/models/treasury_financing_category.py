from odoo import fields, models


class TreasuryFinancingCategory(models.Model):
    _name = "treasury.financing.category"
    _description = "Categoría de financiación"
    _order = "name"

    name = fields.Char(
        required=True,
    )

    category_type = fields.Selection(
        selection=[
            ("income", "Income"),
            ("expense", "Expense"),
        ],
        string="Type",
        required=True,
        default="expense",
    )

    parent_id = fields.Many2one("treasury.financing.category", string="Parent Category")
