# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval


class StockProductionLot(models.Model):
    _inherit = "stock.production.lot"

    repair_order_ids = fields.One2many(
        string="Repairs", comodel_name="repair.order", inverse_name="lot_id", copy=False
    )
    count_repair_orders = fields.Integer(
        string="Count repairs", compute="_compute_count_repair_orders"
    )

    def _compute_count_repair_orders(self):
        for lot in self:
            lot.count_repair_orders = len(lot.repair_order_ids)

    def action_repair_orders_from_lot(self):
        self.ensure_one()
        if not self.repair_order_ids:
            return True
        action = self.env.ref("repair.action_repair_order_tree")
        action_dict = action.read()[0] if action else {}
        domain = expression.AND(
            [
                [("id", "in", self.repair_order_ids.ids)],
                safe_eval(action.domain or "[]"),
            ]
        )
        action_dict.update({"domain": domain})
        return action_dict
