# Copyright 2021 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.osv import expression
from odoo.tools.safe_eval import safe_eval


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    task_count = fields.Integer(
        string="# Tasks",
        compute="_compute_task_count")

    @api.multi
    @api.depends("order_line", "order_line.task_id")
    def _compute_task_count(self):
        for purchase in self:
            purchase.task_count = len(purchase.mapped("order_line.task_id"))

    @api.multi
    def button_open_project_task(self):
        self.ensure_one()
        action = self.env.ref("project.action_view_task")
        action_dict = action.read()[0] if action else {}
        domain = expression.AND([
            [("id", "in", self.mapped(
                "order_line.task_id").ids)],
            safe_eval(action.domain or "[]")])
        action_dict.update({"domain": domain})
        return action_dict
