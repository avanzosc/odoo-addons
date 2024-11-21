from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    manufacturer_id = fields.Many2one(
        "product.manufacturer",
        string="Manufacturer",
        related="product_id.manufacturer_id",
        store=True,
    )
