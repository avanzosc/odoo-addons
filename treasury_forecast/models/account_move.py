from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    estimated_journal_id = fields.Many2one(
        "account.journal",
        string="Estimated Journal",
        domain=[("type", "in", ("bank", "cash"))],
        compute="_compute_estimated_journal",
    )

    @api.depends("payment_mode_id.journal_ids")
    def _compute_estimated_journal(self):
        for move in self:
            journals = move.payment_mode_id.journal_ids
            if len(journals) == 1:
                move.estimated_journal_id = journals[0]
            else:
                move.estimated_journal_id = False
