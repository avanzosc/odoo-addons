# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models
from odoo.tools.float_utils import float_compare


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    def _prepare_stock_moves(self, picking):
        res = super()._prepare_stock_moves(picking)
        price_unit = self._get_stock_move_price_unit()
        qty = self._get_qty_procurement()
        move_dests = self.move_dest_ids
        if not move_dests:
            move_dests = self.move_ids.move_dest_ids.filtered(
                lambda m: m.state != "cancel"
                and not m.location_dest_id.usage == "supplier"
            )
        if not move_dests:
            qty_to_attach = 0
            qty_to_push = self.product_qty - qty
        else:
            move_dests_initial_demand = self.product_id.uom_id._compute_quantity(
                sum(
                    move_dests.filtered(
                        lambda m: m.state != "cancel"
                        and not m.location_dest_id.usage == "supplier"
                    ).mapped("product_qty")
                ),
                self.product_uom,
                rounding_method="HALF-UP",
            )
            qty_to_attach = min(self.product_qty, move_dests_initial_demand) - qty
            qty_to_push = self.product_qty - move_dests_initial_demand
        if (
            float_compare(
                qty_to_attach, 0.0, precision_rounding=self.product_uom.rounding
            )
            == 0
        ):
            product_uom_qty, product_uom = self.product_uom._adjust_uom_quantities(
                qty_to_attach, self.product_id.uom_id
            )
            res.append(
                self._prepare_stock_move_vals(
                    picking, price_unit, product_uom_qty, product_uom
                )
            )
        if (
            float_compare(
                qty_to_push, 0.0, precision_rounding=self.product_uom.rounding
            )
            == 0
        ):
            product_uom_qty, product_uom = self.product_uom._adjust_uom_quantities(
                qty_to_push, self.product_id.uom_id
            )
            extra_move_vals = self._prepare_stock_move_vals(
                picking, price_unit, product_uom_qty, product_uom
            )
            extra_move_vals["move_dest_ids"] = False  # don't attach
            res.append(extra_move_vals)
        return res
