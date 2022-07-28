# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models, fields
from odoo.osv import expression
from odoo.tools.safe_eval import safe_eval


class SaleOrder(models.Model):
    _inherit = "sale.order"

    respair_ids = fields.One2many(
        string="Repairs", comodel_name="repair.order",
        inverse_name="sale_order_id", copy=False)
    repairs_count = fields.Integer(
        string="# Repairs", compute="_compute_repairs_count", copy=False,
        store=True)

    @api.depends("respair_ids")
    def _compute_repairs_count(self):
        for sale in self:
            sale.repairs_count = len(sale.respair_ids)

    def action_repairs_from_sale(self):
        self.ensure_one()
        action = self.env.ref("repair.action_repair_order_tree")
        action_dict = action.read()[0] if action else {}
        domain = expression.AND(
            [
                [("id", "in", self.respair_ids.ids)],
                safe_eval(action.domain or "[]"),
            ]
        )
        action_dict.update({"domain": domain})
        return action_dict

