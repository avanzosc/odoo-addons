# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, models
from odoo.exceptions import ValidationError


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def button_confirm_pickings(self):
        result = super(PurchaseOrder, self).button_confirm_pickings()
        for line in self.order_line:
            if (
                line.product_id
                and (line.product_id.tracking != "none")
                and not (line.lot_id)
                and line.return_qty
            ):
                raise ValidationError(
                    _("The product {} has not lot").format(line.product_id.name)
                )
        return result

    def button_return_picking(self):
        if not self.picking_ids and any(
            [line.product_uom_qty != 0 for line in self.order_line]
        ):
            raise ValidationError(_("First you have to do the delivery."))
        elif not self.picking_ids and any(
            [line.return_qty != 0 for line in self.order_line]
        ):
            if not self.picking_type_id:
                raise ValidationError(_("You must enter the picking type."))
            elif not self.picking_type_id.return_picking_type_id:
                raise ValidationError(
                    _("You must enter the return picking type of picking" " type.")
                )
            else:
                self.button_confirm()
                entry_picking = self.picking_ids[:1]
                entry_picking.button_force_done_detailed_operations()
                pick_type = self.picking_type_id
                picking = self.env["stock.picking"].create(
                    {
                        "partner_id": self.partner_id.id,
                        "picking_type_id": pick_type.return_picking_type_id.id,
                        "location_id": (
                            pick_type.return_picking_type_id.default_location_src_id.id
                            or self.env.ref("stock.stock_location_customers").id
                        ),
                        "location_dest_id": (
                            pick_type.return_picking_type_id.default_location_dest_id.id
                            or self.env.ref("stock.stock_location_suppliers").id
                        ),
                        "company_id": self.company_id.id,
                        "origin": entry_picking.origin,
                    }
                )
                for line in self.order_line:
                    line._prepare_stock_moves(picking)
                for line in entry_picking.move_line_ids_without_package:
                    move = self.env["stock.move"].create(
                        {
                            "purchase_line_id": line.move_id.purchase_line_id.id,
                            "picking_id": picking.id,
                            "product_id": line.product_id.id,
                            "name": line.move_id.name,
                            "product_uom": line.product_uom_id.id,
                            "product_uom_qty": line.move_id.purchase_line_id.return_qty,
                            "location_id": picking.location_id.id,
                            "location_dest_id": picking.location_dest_id.id,
                            "move_orig_ids": [(4, line.move_id.id)],
                            "origin_returned_move_id": line.move_id.id,
                            "to_refund": True,
                            "move_line_ids": [
                                (
                                    0,
                                    0,
                                    {
                                        "picking_id": picking.id,
                                        "product_id": line.product_id.id,
                                        "product_uom_id": line.product_uom_id.id,
                                        "qty_done": line.move_id.purchase_line_id.return_qty,
                                        "location_id": picking.location_id.id,
                                        "location_dest_id": picking.location_dest_id.id,
                                        "lot_id": line.move_id.purchase_line_id.lot_id.id,
                                    },
                                )
                            ],
                        }
                    )
                    line.move_id.write(
                        {
                            "move_dest_ids": [(4, move.id)],
                            "returned_move_ids": [(4, move.id)],
                        }
                    )
                picking.group_id = self.group_id.id
                picking.action_confirm()
                result = picking.button_validate()
                entry_picking.action_cancel()
                entry_picking.sudo().unlink()
                return result
        else:
            picking_act = super(PurchaseOrder, self).button_return_picking()
            picking = self.env["stock.picking"].browse(picking_act.get("res_id"))
            if len(picking) == 1:
                for line in picking.move_line_ids_without_package:
                    if line.move_id.purchase_line_id:
                        line.qty_done = line.move_id.purchase_line_id.return_qty
                if not any([line.return_qty != 0 for line in self.order_line]):
                    return picking_act
                else:
                    picking.action_confirm()
                    return picking.button_validate()
