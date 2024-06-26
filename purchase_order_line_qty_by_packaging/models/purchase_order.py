# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def button_confirm(self):
        result = super().button_confirm()
        for purchase in self:
            for picking in purchase.picking_ids:
                for move in picking.move_ids_without_package:
                    if move.purchase_line_id:
                        for line in move.move_line_ids:
                            line.write(
                                {
                                    "product_packaging_id": move.purchase_line_id.product_packaging.id,
                                    "product_packaging_qty": move.purchase_line_id.product_packaging_qty,
                                }
                            )
        return result
