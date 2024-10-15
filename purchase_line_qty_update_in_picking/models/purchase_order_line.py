# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models
from odoo.tools import float_compare


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    def write(self, values):
        if "product_qty" not in values:
            return super(PurchaseOrderLine, self).write(values)
        return super(
            PurchaseOrderLine,
            self.with_context(product_qty_changed=values.get("product_qty")),
        ).write(values)

    def _prepare_stock_moves(self, picking):
        self.ensure_one()
        vals = super(PurchaseOrderLine, self)._prepare_stock_moves(picking)
        if (
            picking.picking_type_id.code != "incoming"
            or (not vals and "product_qty_changed" not in self.env.context)
            or (vals and "product_qty_changed" in self.env.context)
        ):
            return vals
        res = []
        if self.product_id.type not in ["product", "consu"]:
            return res
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
            < 0
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
            < 0
        ):
            product_uom_qty, product_uom = self.product_uom._adjust_uom_quantities(
                qty_to_push, self.product_id.uom_id
            )
            extra_move_vals = self._prepare_stock_move_vals(
                picking, price_unit, product_uom_qty, product_uom
            )
            extra_move_vals["move_dest_ids"] = False
            res.append(extra_move_vals)
        return res
