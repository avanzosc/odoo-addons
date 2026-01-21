# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare


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

    def _ensure_picking_for_line(
        self, line, qty, picking_type, location_id, location_dest_id, to_refund
    ):
        if qty <= 0:
            return
        picking = line.order_id.picking_ids.filtered(
            lambda p: p.state not in ("done", "cancel")
            and p.picking_type_id == picking_type
        )[:1]
        if not picking:
            vals = line.order_id._prepare_picking(
                picking_type, location_id, location_dest_id
            )
            picking = self.env["stock.picking"].create(vals)
        moves = picking.move_ids_without_package.filtered(
            lambda m: m.purchase_line_id == line and m.state not in ("done", "cancel")
        )
        if moves:
            moves.write(
                {
                    "product_uom_qty": qty,
                    "restrict_lot_id": line.lot_id.id if line.lot_id else False,
                }
            )
        else:
            moves = self.env["stock.move"].create(
                {
                    "name": line.name or line.product_id.display_name,
                    "product_id": line.product_id.id,
                    "product_uom_qty": qty,
                    "product_uom": line.product_uom.id,
                    "picking_id": picking.id,
                    "location_id": location_id,
                    "location_dest_id": location_dest_id,
                    "company_id": line.company_id.id,
                    "purchase_line_id": line.id,
                    "restrict_lot_id": line.lot_id.id if line.lot_id else False,
                    "origin": line.order_id.name,
                    "group_id": line.order_id.group_id.id,
                    "state": "draft",
                }
            )
            if to_refund:
                moves.write(
                    {
                        "to_refund": True,
                    }
                )

    def _create_stock_return_moves(self, picking):
        StockMove = self.env["stock.move"]
        moves = StockMove.browse()
        for line in self:
            qty = line.return_qty - abs(line.qty_received)
            if qty <= 0:
                continue
            moves |= StockMove.create(
                {
                    "name": line.name or line.product_id.display_name,
                    "product_id": line.product_id.id,
                    "product_uom_qty": qty,
                    "product_uom": line.product_uom.id,
                    "picking_id": picking.id,
                    "location_id": line.order_id._get_destination_location(),
                    "location_dest_id": line.order_id.partner_id.property_stock_supplier.id,
                    "company_id": line.order_id.company_id.id,
                    "purchase_line_id": line.id,
                    "restrict_lot_id": line.lot_id.id if line.lot_id else False,
                    "to_refund": True,
                    "origin": line.order_id.name,
                    "group_id": line.order_id.group_id.id,
                    "state": "draft",
                }
            )
        return moves

    def _create_or_update_picking(self):
        for line in self:
            if not (line.product_id and line.product_id.type in ("product", "consu")):
                continue
            if (
                float_compare(
                    line.product_qty, line.qty_received, line.product_uom.rounding
                )
                < 0
                and line.product_qty > 0
            ):
                raise UserError(
                    _(
                        "You cannot decrease the ordered quantity below\n"
                        "the received quantity. Create a return first."
                    )
                )
            if (
                float_compare(
                    line.return_qty, abs(line.qty_received), line.product_uom.rounding
                )
                < 0
                and line.return_qty > 0
            ):
                raise UserError(
                    _(
                        "You cannot decrease the return quantity below\n"
                        "the already returned quantity. Create a reception first."
                    )
                )
            if (
                float_compare(
                    line.product_qty, line.qty_invoiced, line.product_uom.rounding
                )
                == -1
                and line.invoice_lines
            ):
                line.invoice_lines[0].move_id.activity_schedule(
                    "mail.mail_activity_data_warning",
                    note=_(
                        "The quantities on your purchase order indicate less\n"
                        "than billed. You should ask for a refund."
                    ),
                )
            self._ensure_picking_for_line(
                line=line,
                qty=line.product_uom_qty - line.qty_received,
                picking_type=line.order_id.picking_type_id,
                location_id=line.order_id.partner_id.property_stock_supplier.id,
                location_dest_id=line.order_id._get_destination_location(),
                to_refund=False,
            )
            self._ensure_picking_for_line(
                line=line,
                qty=line.return_qty - abs(line.qty_received),
                picking_type=line.order_id.picking_type_id.return_picking_type_id,
                location_id=line.order_id._get_destination_location(),
                location_dest_id=line.order_id.partner_id.property_stock_supplier.id,
                to_refund=True,
            )

    def write(self, values):
        lines = self.filtered(lambda l: l.order_id.state == "purchase")
        prev_product_qty = {line.id: line.product_uom_qty for line in lines}
        prev_return_qty = {line.id: line.return_qty for line in lines}
        res = super().write(values)
        for line in lines:
            if "product_uom_qty" in values:
                if (
                    float_compare(
                        prev_product_qty[line.id],
                        line.product_uom_qty,
                        precision_rounding=line.product_uom.rounding,
                    )
                    != 0
                ):
                    line._create_or_update_picking()
            if "return_qty" in values:
                if (
                    float_compare(
                        prev_return_qty[line.id],
                        line.return_qty,
                        precision_rounding=line.product_uom.rounding,
                    )
                    != 0
                ):
                    line._create_or_update_picking()
        return res

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
