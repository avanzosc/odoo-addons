from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    estimated_journal_id = fields.Many2one(
        "account.journal",
        string="Estimated Journal",
        domain=[("type", "in", ("bank", "cash"))],
    )
