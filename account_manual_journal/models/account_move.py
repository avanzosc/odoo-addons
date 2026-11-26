from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    journal_id = fields.Many2one(
        "account.journal", domain="[('allow_manual_entries','=',True)]", required=True
    )
