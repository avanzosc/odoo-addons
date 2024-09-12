from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    invoice_month = fields.Char(
        related="move_id.invoice_month",
        store=True,
        string="Invoice Month",
    )
    invoice_year = fields.Char(
        related="move_id.invoice_year",
        store=True,
        string="Invoice Year",
    )
    invoice_quarter = fields.Char(
        related="move_id.invoice_quarter",
        store=True,
        string="Invoice Quarter",
    )
