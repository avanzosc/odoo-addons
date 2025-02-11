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
        return super().button_validate()

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
