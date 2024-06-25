# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def button_force_done_detailed_operations(self):
        result = super().button_force_done_detailed_operations()
        for line in self.move_line_ids_without_package:
            line._onchange_product_id()
            line.onchange_standard_price()
        return result

    def action_assign(self):
        result = super().action_assign()
        for move in self.move_ids_without_package:
            if move.standard_price:
                for line in move.move_line_ids:
                    if not line.standard_price:
                        line.standard_price = move.standard_price
        return result

    def button_validate(self):
        result = super().button_validate()
        for line in self.move_line_ids_without_package:
            line.onchange_standard_price()
        return result
