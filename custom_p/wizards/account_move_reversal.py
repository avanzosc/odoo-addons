# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class AccountMoveReversal(models.TransientModel):
    _inherit = "account.move.reversal"

    def reverse_moves(self):
        result = super().reverse_moves()
        model = result.get("res_model")
        if model == "account.move":
            id = result.get("res_id")
            move = self.env[model].browse(id)
            for line in move.invoice_line_ids:
                line.out_refund_from_invoice = True
        return result
