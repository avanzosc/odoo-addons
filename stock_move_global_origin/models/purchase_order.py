# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    global_origin = fields.Char(compute="_compute_global_origin", store=True)

    @api.depends(
        "auto_sale_order_id.global_origin",
        "order_line.move_ids.move_dest_ids.global_origin",
    )
    def _compute_global_origin(self):
        for order in self:
            downstream_origins = order.order_line.move_ids.move_dest_ids.mapped(
                "global_origin"
            )
            order.global_origin = order.auto_sale_order_id.global_origin or next(
                (origin for origin in downstream_origins if origin), False
            )
