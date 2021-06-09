# Copyright 2021 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    @api.multi
    def create_payment_line_from_move_line(self, payment_order):
        move_lines = self.filtered(
            lambda l: l not in payment_order.mapped(
                "payment_line_ids.move_line_id"))
        return super(AccountMoveLine, move_lines
                     ).create_payment_line_from_move_line(payment_order)
