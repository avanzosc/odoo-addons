# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    order_partner_id = fields.Many2one(
        depends=["product_id", "order_id", "order_id.partner_id"]
    )

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

    @api.depends(
        "product_id",
        "order_id.type_id",
        "order_id.type_id.picking_type_id",
        "order_id.type_id.filter_lot_by_location",
        "order_id.type_id.picking_type_id.default_location_src_id",
        "return_qty",
        "product_uom_qty",
    )
    def _compute_possible_lot_ids(self):
        super()._compute_possible_lot_ids()
        for line in self:
            lot_ids = self.env["stock.production.lot"]
            if line.product_id and line.product_id.tracking != "none":
                if line.return_qty and not line.product_uom_qty:
                    lots = self.env["stock.production.lot"].search(
                        [
                            ("product_id", "=", line.product_id.id),
                            ("company_id", "=", line.company_id.id),
                        ]
                    )
                    lot_ids += lots
                    line.possible_lot_ids = [(6, 0, lot_ids.ids)]
