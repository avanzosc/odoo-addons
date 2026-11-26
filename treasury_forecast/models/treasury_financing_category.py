from odoo import fields, models


class TreasuryFinancingCategory(models.Model):
    _name = "treasury.financing.category"
    _description = "Financing category"
    _order = "name"

    name = fields.Char(
        required=True,
    )

    category_type = fields.Selection(
        selection=[
            ("income", "Income"),
            ("expense", "Expense"),
            ("both", "Both"),
        ],
        string="Type",
        required=True,
        default="expense",
    )

    parent_id = fields.Many2one("treasury.financing.category", string="Parent Category")
    child_ids = fields.One2many(
        comodel_name="treasury.financing.category",
        inverse_name="parent_id",
    )
