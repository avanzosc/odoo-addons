# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval


class StockProductionLot(models.Model):
    _inherit = "stock.production.lot"

    mrp_production_ids = fields.One2many(
        string="Manufacturing orders", comodel_name="mrp.production",
        inverse_name="lot_producing_id", copy=False)
    count_mrp_productions = fields.Integer(
        string="Count manufacturing orders",
        compute="_compute_count_mrp_productions")

    def _compute_count_mrp_productions(self):
        for lot in self:
            lot.count_mrp_productions = len(lot.mrp_production_ids)

    def action_manufacturing_orders_from_lot(self):
        self.ensure_one()
        if not self.mrp_production_ids:
            return True
        action = self.env.ref("mrp.mrp_production_action")
        action_dict = action.read()[0] if action else {}
        domain = expression.AND(
            [[("id", "in", self.mrp_production_ids.ids)],
             safe_eval(action.domain or "[]")])
        action_dict.update({"domain": domain})
        return action_dict
