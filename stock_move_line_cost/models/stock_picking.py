# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def _propagate_standard_price_to_move_lines(self):
        for picking in self:
            picking.move_ids._set_standard_price_from_source()
            for move in picking.move_ids:
                move.move_line_ids.filtered(
                    lambda line: not line.standard_price
                ).standard_price = move.standard_price
            picking.move_line_ids.filtered(
                lambda line: not line.standard_price and not line.move_id
            )._set_standard_price_from_source()

    def button_force_done_detailed_operations(self):
        result = super().button_force_done_detailed_operations()
        self._propagate_standard_price_to_move_lines()
        return result

    def action_assign(self):
        result = super().action_assign()
        self._propagate_standard_price_to_move_lines()
        return result

    def button_validate(self):
        result = super().button_validate()
        self._propagate_standard_price_to_move_lines()
        return result
