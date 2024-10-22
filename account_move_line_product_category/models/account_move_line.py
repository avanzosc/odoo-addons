from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    product_category_id = fields.Many2one(
        related="product_id.categ_id",
        string="Product Category",
        store=True,
    )
