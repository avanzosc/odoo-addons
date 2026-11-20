# Copyright 2026 Berezi Amubieta - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    personal_name = fields.Char(
        readonly=True,
        copy=False,
    )

    def _post(self, soft=True):
        posted_moves = super()._post(soft=soft)

        for move in posted_moves.filtered(lambda m: not m.personal_name):
            sequence = self.env["ir.sequence"].with_company(move.company_id)
            seq = sequence.next_by_code(
                "account.move.personal.name",
                sequence_date=move.date,
            )
            move.personal_name = f"{move.date.year}{seq}"

        return posted_moves
