# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    def _prepare_stock_move_vals(
        self, picking, price_unit, product_uom_qty, product_uom
    ):
        self.ensure_one()
        vals = super(PurchaseOrderLine, self)._prepare_stock_move_vals(
            picking, price_unit, product_uom_qty, product_uom
        )
        if self.order_id.picking_type_id.default_location_src_id:
            vals[
                "location_id"
            ] = self.order_id.picking_type_id.default_location_src_id.id
        return vals
