# Copyright 2021 Berezi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval


class ProductTemplate(models.Model):
    _inherit = "product.template"

    density = fields.Float(string="Density")


class ProductProduct(models.Model):
    _inherit = "product.product"

    thermoformed_count = fields.Integer(compute="_compute_thermoformed_count")

    def _compute_thermoformed_count(self):
        thermoformed_obj = self.env["thermoformed.cost"]
        for product in self:
            product.thermoformed_count = thermoformed_obj.search_count(
                [
                    ("variant_id", "=", product.id),
                ]
            )

    def button_open_thermoformed_cost(self):
        self.ensure_one()
        thermoformed_costs = self.env["thermoformed.cost"].search(
            [
                ("variant_id", "=", self.id),
            ]
        )

        action = self.env["ir.actions.actions"]._for_xml_id(
            "thermoformed_cost_calculation.action_thermoformed_cost"
        )
        action["domain"] = expression.AND(
            [
                [("id", "in", thermoformed_costs.ids)],
                safe_eval(action.get("domain") or "[]"),
            ]
        )
        action["context"] = dict(self._context, default_variant_id=self.id)

        return action
