# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models


class AccountMoveReversal(models.TransientModel):
    _inherit = "account.move.reversal"

    def reverse_moves(self):
        self.ensure_one()
        return super(
            AccountMoveReversal, self.with_context(from_reverse_moves=True)
        ).reverse_moves()
