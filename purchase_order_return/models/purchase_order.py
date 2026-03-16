# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, models
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def _create_picking(self):
        for order in self.filtered(lambda o: o.state in ("purchase", "done")):
            has_storable = any(
                p.type in ("product", "consu") for p in order.order_line.product_id
            )
            if has_storable:
                order.order_line.filtered(
                    lambda line: not line.display_type
                )._create_or_update_picking()
        return True

    def _prepare_return_picking(self):
        self.ensure_one()
        return_picking_type = self.picking_type_id.return_picking_type_id
        if not return_picking_type:
            raise UserError(_("The order has no return type configured."))
        return {
            "picking_type_id": return_picking_type.id,
            "partner_id": self.partner_id.id,
            "origin": self.name,
            "location_id": self._get_destination_location(),
            "location_dest_id": self.partner_id.property_stock_supplier.id,
            "company_id": self.company_id.id,
        }

    def button_validate_everything(self):
        for order in self:
            if order.state in ("draft", "sent"):
                order.button_confirm()
            pending_pickings = order.picking_ids.filtered(
                lambda p: p.state not in ("done", "cancel")
            )
            for picking in pending_pickings:
                picking.action_confirm()
                if not picking.move_line_ids:
                    picking.button_force_done_detailed_operations()
            action = pending_pickings.button_validate()
            if isinstance(action, dict):
                return action
        return True
