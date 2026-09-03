# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    picking_type_sequence_code = fields.Char(
        related="picking_type_id.sequence_code", store=True
    )

    global_origin = fields.Char(
        compute="_compute_global_origin", store=True, index=True
    )

    @api.depends(
        "sale_line_id.order_id.global_origin",
        "purchase_line_id.order_id.global_origin",
        "raw_material_production_id.global_origin",
        "production_id.global_origin",
        "move_orig_ids.global_origin",
        "move_dest_ids.global_origin",
    )
    def _compute_global_origin(self):
        for move in self:
            move.global_origin = (
                move.sale_line_id.order_id.global_origin
                or move.purchase_line_id.order_id.global_origin
                or move.raw_material_production_id.global_origin
                or move.production_id.global_origin
                or next(
                    (
                        origin
                        for origin in move.move_orig_ids.mapped("global_origin")
                        if origin
                    ),
                    False,
                )
                or next(
                    (
                        origin
                        for origin in move.move_dest_ids.mapped("global_origin")
                        if origin
                    ),
                    False,
                )
            )
