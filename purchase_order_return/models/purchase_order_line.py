# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


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
    def create(self, vals):
        line = super().create(vals)
        if line.order_id.state == "purchase":
            line._apply_line_quantities()
        return line

    def write(self, values):
        for line in self:
            if "return_qty" in values:
                new_return_qty = values["return_qty"]
                if new_return_qty < abs(line.qty_received):
                    done_return_moves = line.move_ids.filtered(
                        lambda m: m.state == "done"
                        and m.location_dest_id.usage in ("customer", "supplier")
                        and m.location_id.usage == "internal"
                        and not m.scrapped
                    )
                    if done_return_moves:
                        raise ValidationError(
                            _("Some qtys were already returned, qty can't be reduced.")
                        )
        res = super(PurchaseOrderLine, self).write(values)
        if (
            ("return_qty" in values and values["return_qty"] > 0)
            or ("product_qty" in values and values["product_qty"] > 0)
        ) and line.order_id.state == "purchase":
            self._apply_line_quantities()
        return res

    def _apply_line_quantities(self):
        for line in self:
            if line.return_qty > 0:
                line._apply_return_quantity()
            if line.product_qty > 0:
                line._apply_receipt_quantity()

    def _apply_receipt_quantity(self):
        self.ensure_one()
        qty_to_receive = self.product_qty - self.qty_received
        if qty_to_receive <= 0:
            return
        picking = self._find_pending_picking("incoming")
        if not picking:
            picking = self.env["stock.picking"].create(self.order_id._prepare_picking())
        move = self._find_or_create_move(picking, qty_to_receive)
        self._prepare_move_lines(move)
        move.picking_id.button_force_done_detailed_operations()

    def _apply_return_quantity(self):
        self.ensure_one()
        qty_to_return = abs(self.return_qty) - abs(self.qty_received)
        if qty_to_return <= 0:
            return
        picking = self._find_pending_picking("outgoing")
        if not picking:
            picking = self.env["stock.picking"].create(
                self.order_id._prepare_return_picking()
            )
        move = self._find_or_create_move(picking, qty_to_return, is_return=True)
        self._prepare_move_lines(move)
        move.picking_id.button_force_done_detailed_operations()

    def _find_pending_picking(self, picking_type_code):
        return self.order_id.picking_ids.filtered(
            lambda p: p.state not in ("done", "cancel")
            and p.picking_type_id.code == picking_type_code
        )[:1]

    def _find_or_create_move(self, picking, qty, is_return=False):
        move = picking.move_ids_without_package.filtered(
            lambda m: m.purchase_line_id == self and m.state not in ("done", "cancel")
        )[:1]
        if move:
            if move.move_line_ids:
                move.move_line_ids.unlink()
            move.product_uom_qty = qty
            return move
        return self.env["stock.move"].create(
            {
                "name": self.name,
                "product_id": self.product_id.id,
                "product_uom_qty": qty,
                "product_uom": self.product_uom.id,
                "picking_id": picking.id,
                "picking_type_id": picking.picking_type_id.id,
                "location_id": picking.location_id.id,
                "location_dest_id": picking.location_dest_id.id,
                "purchase_line_id": self.id,
                "to_refund": is_return,
            }
        )

    def _prepare_move_lines(self, move):
        if move.state == "draft":
            move._action_confirm()
        for ml in move.move_line_ids:
            if move.purchase_line_id.lot_id:
                ml.lot_id = move.purchase_line_id.lot_id.id

    @api.depends(
        "move_ids.state",
        "move_ids.scrapped",
        "move_ids.product_uom_qty",
        "move_ids.product_uom",
        "return_qty",
        "move_ids.quantity_done",
    )
    def _compute_qty_received(self):
        super(PurchaseOrderLine, self)._compute_qty_received()
        for line in self:
            if line.return_qty and line.return_qty > 0:
                line.product_qty = line.qty_received

    def _create_or_update_picking(self):
        return True
