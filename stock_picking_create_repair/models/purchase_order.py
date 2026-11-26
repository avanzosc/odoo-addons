# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models
from odoo.osv import expression
from odoo.tools.safe_eval import safe_eval


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    is_repair = fields.Boolean(
        string="It's repair",
        default=False,
        copy=False,
    )
    repair_ids = fields.One2many(
        string="Repairs",
        comodel_name="repair.order",
        inverse_name="purchase_order_id",
        copy=False,
    )
    repairs_count = fields.Integer(
        string="# Repairs",
        compute="_compute_repairs_count",
        copy=False,
        store=True,
    )

    @api.depends("repair_ids")
    def _compute_repairs_count(self):
        for purchase in self:
            purchase.repairs_count = len(purchase.repair_ids)

    def action_repairs_from_purchase(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id(
            "repair.action_repair_order_tree"
        )
        action["domain"] = expression.AND(
            [
                [("id", "in", self.repair_ids.ids)],
                safe_eval(action.get("domain") or "[]"),
            ]
        )
        return action

    def _prepare_picking(self):
        vals = super()._prepare_picking()
        vals["is_repair"] = self.is_repair
        return vals
