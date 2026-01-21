# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import SUPERUSER_ID, _, models
from odoo.exceptions import UserError, ValidationError


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def button_validate_everything(self):
        for order in self:
            for line in order.order_line:
                if (
                    line.return_qty > 0
                    and line.product_id.tracking != "none"
                    and not line.lot_id
                ):
                    raise ValidationError(
                        _("The product {} has not lot").format(line.product_id.name)
                    )
            if order.state in ["draft", "sent"]:
                order.button_confirm()
            pickings = order.picking_ids.filtered(
                lambda p: p.state not in ("done", "cancel")
            )
            if pickings:
                for picking in pickings:
                    picking.action_confirm()
                    action = picking.button_validate()
                    if isinstance(action, dict):
                        return action
        return True

    def _prepare_picking(self, picking_type, location_id, location_dest_id):
        if not self.group_id:
            self.group_id = self.group_id.create(
                {"name": self.name, "partner_id": self.partner_id.id}
            )
        if not self.partner_id.property_stock_supplier.id:
            raise UserError(
                _("You must set a Vendor Location for this partner %s")
                % self.partner_id.name
            )
        return {
            "picking_type_id": picking_type.id,
            "partner_id": self.partner_id.id,
            "user_id": False,
            "date": self.date_order,
            "origin": self.name,
            "location_id": location_id,
            "location_dest_id": location_dest_id,
            "company_id": self.company_id.id,
        }

    def _process_picking(
        self,
        lines,
        existing_pickings,
        picking_type,
        location_id,
        location_dest_id,
        is_return=False,
    ):
        StockPicking = self.env["stock.picking"]
        if not lines:
            return False
        if not existing_pickings:
            res = self._prepare_picking(picking_type, location_id, location_dest_id)
            picking = StockPicking.with_user(SUPERUSER_ID).create(res)
        else:
            picking = existing_pickings[0]
        if is_return:
            moves = lines._create_stock_return_moves(picking)
        else:
            moves = lines._create_stock_moves(picking)
        moves = moves.filtered(
            lambda m: m.state not in ("done", "cancel")
        )._action_confirm()
        seq = 0
        for move in sorted(moves, key=lambda m: m.date):
            seq += 5
            move.sequence = seq
        moves._action_assign()
        picking.message_post_with_view(
            "mail.message_origin_link",
            values={"self": picking, "origin": self},
            subtype_id=self.env.ref("mail.mt_note").id,
        )
        return picking

    def _create_picking(self):
        for order in self.filtered(lambda po: po.state in ("purchase", "done")):
            if not any(
                product.type in ["product", "consu"]
                for product in order.order_line.product_id
            ):
                continue
            order = order.with_company(order.company_id)
            entry_pickings = order.picking_ids.filtered(
                lambda p: p.state not in ("done", "cancel")
                and p.picking_type_id == order.picking_type_id
            )
            return_pickings = order.picking_ids.filtered(
                lambda p: p.state not in ("done", "cancel")
                and p.picking_type_id == order.picking_type_id.return_picking_type_id
            )
            entry_lines = order.order_line.filtered(
                lambda l: (l.product_uom_qty - l.qty_received) > 0
            )
            return_lines = order.order_line.filtered(
                lambda l: (l.return_qty - abs(l.qty_received)) > 0
            )
            location_dest = order._get_destination_location()
            location_id = order.partner_id.property_stock_supplier.id
            picking_type = order.picking_type_id
            order._process_picking(
                entry_lines,
                entry_pickings,
                picking_type=picking_type,
                location_id=location_id,
                location_dest_id=location_dest,
            )
            order._process_picking(
                return_lines,
                return_pickings,
                picking_type=picking_type.return_picking_type_id,
                location_id=location_dest,
                location_dest_id=location_id,
                is_return=True,
            )
        return True
