# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval


class StockPickingBatch(models.Model):
    _inherit = "stock.picking.batch"

    sale_order_ids = fields.Many2many(
        string="Sale Orders",
        comodel_name="sale.order",
        compute="_compute_sale_orders",
    )
    count_sale_orders = fields.Integer(
        string="Num. Sale Orders", compute="_compute_sale_orders"
    )

    def _compute_sale_orders(self):
        for batch in self:
            sale_orders = batch.mapped("picking_ids.sale_id")
            batch.sale_order_ids = [(6, 0, sale_orders.ids)]
            batch.count_sale_orders = len(sale_orders)

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
