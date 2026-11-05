# Copyright 2026 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockProductionLot(models.Model):
    _inherit = "stock.production.lot"

    average_price = fields.Float(
        string="Average Price",
        compute="_compute_average_price",
    )

    @api.depends(
        "move_line_ids.amount",
        "move_line_ids.qty_done",
        "move_line_ids.state",
        "move_line_ids.location_id",
        "move_line_ids.location_dest_id",
        "move_line_ids.location_id.usage",
        "move_line_ids.location_dest_id.usage",
    )
    def _compute_average_price(self):
        for lot in self:
            internal_lines = lot.move_line_ids.filtered(
                lambda line: (
                    line.state == "done"
                    and line.location_dest_id.usage == "internal"
                    and line.location_id.usage != "internal"
                )
            )

            amount_total = sum(internal_lines.mapped("amount"))
            qty_done = sum(internal_lines.mapped("qty_done"))

            lot.average_price = amount_total / qty_done if qty_done else 0.0
