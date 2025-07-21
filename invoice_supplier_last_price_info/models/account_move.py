# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def action_post(self):
        result = super().action_post()
        for move in self.filtered(
            lambda x: x.state == "posted" and x.move_type == "in_invoice"
        ):
            for line in move.invoice_line_ids.filtered(
                lambda z: z.display_type == "product"
            ):
                line.product_id.set_product_last_supplier_move(move.id)
        return result

    def button_cancel(self):
        result = super().button_cancel()
        for move in self.filtered(
            lambda x: x.state == "cancel" and x.move_type == "in_invoice"
        ):
            for line in move.invoice_line_ids.filtered(
                lambda z: z.display_type == "product"
            ):
                line.product_id.set_product_last_supplier_move()
        return result
