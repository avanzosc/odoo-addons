from odoo import fields, models


class AccountJournal(models.Model):
    _inherit = "account.journal"

    allow_manual_entries = fields.Boolean(
        help="Enable this journal to be used when creating manual journal entries"
    )
