# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    product_qty = fields.Float(
        required=False,
    )
    return_qty = fields.Float(
        string="Return Qty",
    )

    @api.onchange("product_id", "company_id")
    def onchange_product_id(self):
        result = super(PurchaseOrderLine, self).onchange_product_id()
        if self.product_qty == 1 and not self.intercompany_sale_line_id:
            self.product_qty = 0
        return result

    @api.model
    def create(self, values):
        line = super().create(values)
        if "return_qty" in values:
            done_picking = line.order_id.picking_ids.filtered(
                lambda c: c.state == "done"
            )
            if done_picking:
                for move in line.move_ids:
                    if move.picking_id != done_picking[:1]:
                        picking = move.picking_id
                        move.picking_id = done_picking[:1].id
                        move.state = "done"
                        if not move.move_line_ids:
                            self.env["stock.move.line"].create(
                                move._prepare_move_line_vals()
                            )
                        if not picking.move_ids_without_package:
                            picking.unlink()
        return line
