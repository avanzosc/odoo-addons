from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    estimated_journal_id = fields.Many2one(
        "account.journal",
        string="Estimated Journal",
        related="move_id.estimated_journal_id",
        store=True,
        readonly=True,
    )

    product_category_id = fields.Many2one(
        comodel_name="product.category",
        string="Product Category",
        related="product_id.categ_id",
        store=True,
        readonly=True,
    )
