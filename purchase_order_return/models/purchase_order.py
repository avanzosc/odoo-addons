# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, models
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def _create_picking(self):
        return self.env["stock.picking"]

    def button_approve(self, force=False):
        res = super().button_approve(force=force)
        for order in self:
            for line in order.order_line:
                line._apply_line_quantities()
        return res

    def _prepare_return_picking(self):
        self.ensure_one()

        picking_type = self.picking_type_id.return_picking_type_id

        if not picking_type:
            raise UserError(_("The order has no return type configured."))

        return {
            "picking_type_id": picking_type.id,
            "partner_id": self.partner_id.id,
            "origin": self.name,
            "location_id": self._get_destination_location(),
            "location_dest_id": self.partner_id.property_stock_supplier.id,
            "company_id": self.company_id.id,
        }

    def button_validate_everything(self):
        for order in self:
            if order.state in ["draft", "sent"]:
                order.button_confirm()
            pending_pickings = order.picking_ids.filtered(
                lambda p: p.state not in ("done", "cancel")
            )
            for picking in pending_pickings:
                picking.action_confirm()
                picking.button_force_done_detailed_operations()
            action = pending_pickings.button_validate()
            if isinstance(action, dict):
                return action
        return True

    def button_confirm(self):
        res = super().button_confirm()
        for order in self:
            pending_pickings = order.picking_ids.filtered(
                lambda p: p.state not in ("done", "cancel")
            )
            for picking in pending_pickings:
                picking.action_confirm()
                picking.button_force_done_detailed_operations()
        return res
