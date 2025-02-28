# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class StockPicking(models.Model):
    _inherit = "stock.picking"
    _order = "custom_date_done desc, priority desc, scheduled_date asc, id desc"

    def button_validate(self):
        for picking in self:
            if not picking.crm_driver_id:
                picking.crm_driver_id = self.env.user.partner_id.id
        result = super().button_validate()
        for record in self.sudo():
            dest_company = (
                record.sale_id.partner_id.commercial_partner_id.ref_company_ids
            )
            if (
                dest_company
                and dest_company.sync_picking
                and record.state == "done"
                and record.picking_type_code == "incoming"
            ):
                if record.intercompany_picking_id:
                    dest_picking = record.intercompany_picking_id
                    for line in dest_picking.move_line_ids_without_package:
                        line.unlink()
                    dest_picking.button_force_done_detailed_operations()
                    dest_move_qty_update_dict = {}
                    for move in record.move_ids_without_package.sudo():
                        dest_move = (
                            move.sale_line_id.auto_purchase_line_id.move_ids.filtered(
                                lambda x, pick=dest_picking: x.picking_id == pick
                            )
                        )
                        for line, dest_line in zip(
                            move.move_line_ids, dest_move.move_line_ids
                        ):
                            dest_line.sudo().write(
                                {
                                    "qty_done": line.qty_done,
                                }
                            )
                        dest_move_qty_update_dict.setdefault(dest_move, 0.0)
                        dest_move_qty_update_dict[dest_move] += move.quantity_done
                    for dest_move, qty_done in dest_move_qty_update_dict.items():
                        dest_move.quantity_done = qty_done
                    dest_picking.sudo().with_context(
                        cancel_backorder=bool(
                            self.env.context.get("picking_ids_not_to_backorder")
                        )
                    )._action_done()
        return result

    def _action_done_intercompany_actions(self, purchase):
        pick = self
        for move in pick.move_lines:
            move_lines = move.move_line_ids
            po_move_lines = move.sale_line_id.auto_purchase_line_id.move_ids.filtered(
                lambda x, ic_pick=pick.intercompany_picking_id: (
                    x.picking_id == ic_pick
                )
            ).mapped("move_line_ids")
            if len(move_lines) != len(po_move_lines) and po_move_lines:
                while len(move_lines) > len(po_move_lines):
                    po_move_lines[:1].copy()
                    po_move_lines = (
                        move.sale_line_id.auto_purchase_line_id.move_ids.filtered(
                            lambda x, ic_pick=pick.intercompany_picking_id: x.picking_id
                            == ic_pick
                        ).mapped("move_line_ids")
                    )
        return super()._action_done_intercompany_actions(purchase=purchase)
