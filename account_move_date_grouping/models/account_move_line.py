from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    invoice_month = fields.Char(
        related="move_id.invoice_month",
        store=True,
    )
    invoice_year = fields.Char(
        related="move_id.invoice_year",
        store=True,
    )
    invoice_quarter = fields.Char(
        related="move_id.invoice_quarter",
        store=True,
    )
