# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def lines_grouped_by_picking(self):
        self.ensure_one()
        print("************************")
        print("*** self.move_type: " + str(self.move_type))
        if self.move_type != "out_refund":
            return super().lines_grouped_by_picking()

        result = []
        for line in self.invoice_line_ids.filtered(lambda x: not x.display_type):
            result.append(
                {
                    "picking": self.env["stock.picking"],
                    "line": line,
                    "quantity": line.quantity,
                }
            )
        return result
