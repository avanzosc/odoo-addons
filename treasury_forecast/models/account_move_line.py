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
