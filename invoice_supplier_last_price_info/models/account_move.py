# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def action_move_open(self):
        result = super().action_move_open()
        for move in self.filtered(lambda x: x.state == "open" and x.type == "in_move"):
            for line in move.move_line_ids:
                line.product_id.set_product_last_supplier_move(move.id)
        return result

    def action_move_cancel(self):
        result = super().action_move_cancel()
        for move in self.filtered(
            lambda x: x.state == "cancel" and x.type == "in_move"
        ):
            for line in move.move_line_ids:
                line.product_id.set_product_last_supplier_move()
        return result
