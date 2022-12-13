# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval


class StockPickingBatch(models.Model):
    _inherit = "stock.picking.batch"

    sale_order_ids = fields.Many2many(
        string="Sale Orders", compute="_compute_sale_order_ids")
    count_sale_orders = fields.Integer(
        string="Num. Sale Orders", compute="_compute_count_sale_orders")
    count_pickings = fields.Integer(
        string="Num. Pickings", compute="_compute_count_pickings")

    def _compute_sale_order_ids(self):
        for batch in self:
            sale_orders = self.env["sale.order"]
            if batch.move_ids:
                move_lines = batch.move_ids.filtered(lambda x: x.sale_line_id)
                if move_lines:
                    sale_lines = move_lines.mapped("sale_line_id")
                    sale_orders = sale_lines.mapped("order_id")
            batch.sale_order_ids = [(6, 0, sale_orders.ids)]

    def _compute_count_sale_orders(self):
        for batch in self:
            batch.count_sale_orders = len(batch.sale_order_ids)

    def _compute_count_pickings(self):
        for batch in self:
            batch.count_pickings = len(batch.picking_ids)

    def action_view_pickings(self):
        action = self.env.ref("stock.action_picking_tree_all")
        action_dict = action and action.read()[0]
        domain = expression.AND(
            [
                [("id", "in", self.picking_ids.ids)],
                safe_eval(action.domain or "[]"),
            ]
        )
        action_dict.update({"domain": domain})
        return action_dict

    def action_view_sale_orders(self):
        action = self.env.ref("sale.action_quotations")
        action_dict = action and action.read()[0]
        domain = expression.AND(
            [
                [("id", "in", self.sale_order_ids.ids)],
                safe_eval(action.domain or "[]"),
            ]
        )
        action_dict.update({"domain": domain})
        return action_dict
