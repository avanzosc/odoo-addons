from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    category_id = fields.Many2one(
        related="product_id.categ_id",
        string="Variant Category",
        store=True,
        readonly=True,
    )
