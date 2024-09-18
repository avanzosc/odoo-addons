# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def lines_grouped_by_picking(self):
        result = super().lines_grouped_by_picking()
        if self.move_type == "out_refund":
            result = []
            for line in self.invoice_line_ids.sorted(lambda l: l.sequence):
                result.append(
                    {
                        "picking": self.env["stock.picking"],
                        "line": line,
                        "quantity": line.quantity,
                    }
                )
        return result
