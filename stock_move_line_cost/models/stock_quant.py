# Copyright 2025 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class StockQuant(models.Model):
    _inherit = "stock.quant"

    def _get_inventory_cost(self):
        return self.product_id.standard_price or 0.0

    def _get_inventory_move_values(self, qty, location_id, location_dest_id, out=False):
        """Called when user manually set a new quantity (via `inventory_quantity`)
        just before creating the corresponding stock move.
        :param location_id: `stock.location`
        :param location_dest_id: `stock.location`
        :param out: boolean to set on True when the move go to inventory adjustment location.
        :return: dict with all values needed to create a new `stock.move` with its move line.
        """
        vals = super()._get_inventory_move_values(
            qty, location_id, location_dest_id, out=out
        )

        cost = self._get_inventory_cost()

        move_lines = vals.get("move_line_ids", [])
        move_qty_done = 0.0

        for _, _, move_line_vals in move_lines:
            qty_done = abs(move_line_vals.get("qty_done", 0.0))
            move_line_vals.update(
                {
                    "standard_price": cost,
                    "amount": cost * qty_done,
                }
            )
            move_qty_done += qty_done

        vals.update(
            {
                "standard_price": cost,
                "amount": cost * move_qty_done,
            }
        )

        return vals
