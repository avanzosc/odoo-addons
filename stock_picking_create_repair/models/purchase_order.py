# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models, fields
from odoo.osv import expression
from odoo.tools.safe_eval import safe_eval


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    is_repair = fields.Boolean(
        string="It's repair", default=False, copy=False)
    respair_ids = fields.One2many(
        string="Repairs", comodel_name="repair.order",
        inverse_name="purchase_order_id", copy=False)
    repairs_count = fields.Integer(
        string="# Repairs", compute="_compute_repairs_count", copy=False,
        store=True)

    @api.depends("respair_ids")
    def _compute_repairs_count(self):
        for purchase in self:
            purchase.repairs_count = len(purchase.respair_ids)

    def action_repairs_from_purchase(self):
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

    def _prepare_picking(self):
        vals = super(PurchaseOrder, self)._prepare_picking()
        vals['is_repair'] = self.is_repair
        return vals
