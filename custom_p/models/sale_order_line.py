# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.depends(
        "move_ids.state",
        "move_ids.scrapped",
        "move_ids.product_uom_qty",
        "move_ids.product_uom",
    )
    def _compute_qty_delivered(self):
        super()._compute_qty_delivered()
        for line in self:
            if (
                line.qty_delivered_method == "stock_move"
                and (line.order_id.update_line_qty)
                and line.return_qty
            ):
                line.product_uom_qty = line.qty_delivered
            if (
                len(line.order_id.picking_ids) > 1
                and line.order_id.update_line_qty
                and all([c.state == "done" for c in line.order_id.picking_ids])
                and all(
                    [
                        c.product_uom_qty == c.qty_delivered
                        for c in (line.order_id.order_line)
                    ]
                )
            ):
                line.order_id.update_line_qty = False
