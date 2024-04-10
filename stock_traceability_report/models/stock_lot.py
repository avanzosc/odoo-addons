# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, fields, models


class StockLot(models.Model):
    _inherit = "stock.lot"

    stock_move_line_ids = fields.One2many(
        comodel_name="stock.move.line",
        string="Product Moves",
        compute="_compute_move_line_ids",
    )
    stock_move_ids = fields.One2many(
        comodel_name="stock.move",
        string="Stock Moves",
        compute="_compute_move_ids",
        domain=[("state", "=", "done")],
    )

    def _compute_move_ids(self):
        for record in self:
            record.stock_move_ids = record.stock_move_line_ids.mapped("move_id").ids

    def _compute_move_line_ids(self):
        for record in self:
            move_lines = self.env["stock.move.line"].search(
                [("lot_id", "=", record.id)]
            )
            record.stock_move_line_ids = move_lines.ids

    def action_view_stock_move_lines(self):
        self.ensure_one()
        action_window = {
            "name": _("Stock Move Lines"),
            "type": "ir.actions.act_window",
            "res_model": "stock.move.line",
            "view_mode": "tree,form",
            "domain": [("id", "in", self.stock_move_line_ids.ids)],
        }
        return action_window
