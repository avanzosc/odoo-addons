# Copyright 2020 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    product_code = fields.Char(
        string="Product Code", compute="_compute_product_code", store=True, copy=False
    )

    @api.depends("picking_id", "product_id", "product_uom_qty")
    def _compute_product_code(self):
        for move in self:
            product_code = ""
            if (
                move.product_id
                and move.product_id.seller_ids
                and move.picking_id
                and move.picking_id.picking_type_id.code == "incoming"
            ):
                seller = move.product_id._select_seller(
                    partner_id=move.picking_id.partner_id,
                    quantity=move.product_uom_qty,
                    uom_id=move.product_uom,
                )
                if seller and seller.product_code:
                    product_code = seller.product_code
                else:
                    if move.product_id.default_code:
                        product_code = move.product_id.default_code
            move.product_code = product_code
