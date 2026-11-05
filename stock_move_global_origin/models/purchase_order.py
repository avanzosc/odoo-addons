# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    global_origin = fields.Char(
        compute="_compute_global_origin", store=True, index=True, recursive=True
    )

    @api.depends(
        "auto_sale_order_id.global_origin",
        "order_line.move_dest_ids.global_origin",
        "order_line.move_ids.move_dest_ids.global_origin",
        "order_line.move_ids.move_dest_ids.purchase_line_id",
        "order_line.sale_line_id.order_id.global_origin",
    )
    def _compute_global_origin(self):
        for order in self:
            demand_moves = (
                order.order_line.move_dest_ids | order.order_line.move_ids.move_dest_ids
            ).filtered(
                lambda move, order=order: move.purchase_line_id.order_id != order
                and move._is_global_origin_demand()
            )
            origins = (
                order.auto_sale_order_id.mapped("global_origin")
                + demand_moves.mapped("global_origin")
                + order.order_line.sale_line_id.order_id.mapped("global_origin")
            )
            order.global_origin = next((origin for origin in origins if origin), False)
