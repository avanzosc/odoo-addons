# Copyright 2023 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    count_lots = fields.Integer(
        string="Lots",
        compute="_compute_count_lots",
    )

    def _compute_count_lots(self):
        for picking in self:
            lines = picking.move_line_ids.filtered(lambda x: x.lot_id)
            picking.count_lots = 0 if not lines else len(lines.mapped("lot_id"))

    def action_picking_move_line_tree(self):
        action = self.env["ir.actions.actions"]._for_xml_id(
            "stock.stock_move_line_action"
        )
        action["context"] = self.env.context
        action["domain"] = [("picking_id", "in", self.ids)]
        return action

    def action_picking_stock_production_lot_tree(self):
        lines = self.move_line_ids.filtered(lambda x: x.lot_id)
        lots = lines.mapped("lot_id")
        action = self.env["ir.actions.actions"]._for_xml_id(
            "stock.action_production_lot_form"
        )
        action["context"] = self.env.context
        action["domain"] = [("id", "in", lots.ids)]
        return action
