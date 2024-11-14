# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    category_type_id = fields.Many2one(
        string="Product Section",
        comodel_name="category.type",
        related="product_id.category_type_id",
        store=True,
    )

    @api.depends("move_ids.state", "move_ids.product_uom_qty", "move_ids.product_uom")
    def _compute_qty_received(self):
        super()._compute_qty_received()
        for line in self:
            if (
                line.qty_received_method == "stock_moves"
                and line.return_qty
                and line.order_id.update_line_qty
            ):
                line.product_qty = line.qty_received
            if (
                len(line.order_id.picking_ids) > 1
                and line.order_id.update_line_qty
                and all([c.state == "done" for c in line.order_id.picking_ids])
                and all(
                    [
                        c.product_qty == c.qty_received
                        for c in (line.order_id.order_line)
                    ]
                )
            ):
                line.order_id.update_line_qty = False

    def _create_or_update_picking(self):
        for line in self:
            if (
                line.product_id
                and line.product_id.type in ("product", "consu")
                and line.order_id.update_line_qty
                and line.return_qty
            ):
                continue
            else:
                return super()._create_or_update_picking()
