# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

RETURN_LOCATION_USAGES = ("customer", "supplier")


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    product_qty = fields.Float(required=False)
    return_qty = fields.Float(string="Return Qty")

    @api.onchange("product_id", "company_id")
    def onchange_product_id(self):
        result = super().onchange_product_id()
        if self.product_qty == 1 and not self.intercompany_sale_line_id:
            self.product_qty = 0
        return result

    def write(self, values):
        if "return_qty" in values:
            self._check_return_qty_reduction(values["return_qty"])
        res = super().write(values)
        if "return_qty" in values and not self.env.context.get("skip_picking_sync"):
            for line in self.filtered(
                lambda line: line.order_id.state == "purchase" and line.return_qty > 0
            ):
                line._create_or_update_return_picking()
        return res

    def _check_return_qty_reduction(self, new_return_qty):
        for line in self:
            if new_return_qty >= abs(line.qty_received):
                continue
            done_return_moves = line.move_ids.filtered(
                lambda m: (
                    m.state == "done"
                    and m.location_dest_id.usage in RETURN_LOCATION_USAGES
                    and m.location_id.usage == "internal"
                    and not m.scrapped
                )
            )
            if done_return_moves:
                raise ValidationError(
                    _("Some qtys were already returned, qty can't be reduced.")
                )

    def _create_or_update_picking(self):
        for line in self:
            if not line.product_id or line.product_id.type not in ("product", "consu"):
                continue
            if line.return_qty > 0:
                line._create_or_update_return_picking()
                picking_type_code = "outgoing"
            elif line.product_qty > 0:
                super(PurchaseOrderLine, line)._create_or_update_picking()
                picking_type_code = "incoming"
            else:
                continue
            pending_picking = line._get_pending_picking(picking_type_code)
            if pending_picking:
                pending_picking.do_unreserve()

    def _create_or_update_return_picking(self):
        self.ensure_one()
        existing_return_qty = self._compute_existing_return_qty()
        qty_to_add = self.return_qty - existing_return_qty
        if qty_to_add <= 0:
            self._adjust_pending_return_picking()
            return
        picking = self._get_pending_picking("outgoing") or self.env[
            "stock.picking"
        ].create(self.order_id._prepare_return_picking())
        self._update_or_create_return_move(picking, qty_to_add)

    def _compute_existing_return_qty(self):
        return sum(
            m.product_uom._compute_quantity(m.product_uom_qty, self.product_uom)
            for m in self.move_ids
            if (
                m.state != "cancel"
                and m.location_dest_id.usage in RETURN_LOCATION_USAGES
                and not m.scrapped
            )
        )

    def _get_pending_picking(self, picking_type_code):
        return self.order_id.picking_ids.filtered(
            lambda p: (
                p.state not in ("done", "cancel")
                and p.picking_type_id.code == picking_type_code
            )
        )[:1]

    def _adjust_pending_return_picking(self):
        pending_picking = self._get_pending_picking("outgoing")
        if not pending_picking:
            return
        pending_move = self.move_ids.filtered(
            lambda m: (
                m.picking_id == pending_picking and m.state not in ("done", "cancel")
            )
        )[:1]
        if not pending_move:
            return
        already_returned_qty = sum(
            m.product_uom._compute_quantity(m.product_uom_qty, self.product_uom)
            for m in self.move_ids
            if (
                m.state == "done"
                and m.location_dest_id.usage in RETURN_LOCATION_USAGES
                and not m.scrapped
            )
        )
        remaining_qty = self.return_qty - already_returned_qty
        if remaining_qty > 0:
            pending_move.product_uom_qty = remaining_qty

    def _update_or_create_return_move(self, picking, qty_to_return):
        pending_move = self.move_ids.filtered(
            lambda m: m.picking_id == picking and m.state not in ("done", "cancel")
        )[:1]
        if pending_move:
            pending_move.product_uom_qty += qty_to_return
        else:
            pending_move = self.env["stock.move"].create(
                {
                    "name": self.name,
                    "product_id": self.product_id.id,
                    "product_uom_qty": qty_to_return,
                    "product_uom": self.product_uom.id,
                    "picking_id": picking.id,
                    "picking_type_id": picking.picking_type_id.id,
                    "location_id": picking.location_id.id,
                    "location_dest_id": picking.location_dest_id.id,
                    "purchase_line_id": self.id,
                    "to_refund": True,
                }
            )
        pending_move._action_confirm()

    def _create_stock_moves(self, picking):
        if picking.picking_type_id.code == "outgoing":
            return self.env["stock.move"]
        return super()._create_stock_moves(picking)

    def _track_qty_received(self, new_qty):
        self.ensure_one()
        previous_qty = self.qty_received
        super()._track_qty_received(new_qty)
        if not new_qty or new_qty == previous_qty or self.qty_to_receive > 0:
            return
        if self.return_qty > 0:
            vals = {"product_qty": new_qty, "return_qty": abs(new_qty)}
        elif self.product_qty:
            vals = {"product_qty": new_qty}
        else:
            return
        self.with_context(skip_picking_sync=True).write(vals)
