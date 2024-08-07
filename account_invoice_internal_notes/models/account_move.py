from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    internal_notes = fields.Text(
        tracking=True,
    )
