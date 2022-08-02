# Copyright 2022 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval


class ProjectTask(models.Model):
    _inherit = "project.task"

    timesheet_ids = fields.One2many(
        domain=[("project_id", "!=", False)],
    )
    analytic_line_ids = fields.One2many(
        string="Analytic Lines",
        comodel_name="account.analytic.line",
        inverse_name="task_id",
        domain=[("project_id", "=", False)],
        readonly=True,
    )
    picking_ids = fields.One2many(
        comodel_name="stock.picking",
        inverse_name="task_id",
        string="Pickings",
    )
    picking_count = fields.Integer(
        compute="_compute_picking_count",
        string="# Pickings",
    )

    def _compute_picking_count(self):
        for task in self:
            task.picking_count = len(task.picking_ids)

    def button_open_pickings(self):
        self.ensure_one()
        action = self.env.ref("stock.stock_picking_action_picking_type")
        action_dict = action and action.read()[0]
        domain = expression.AND(
            [
                [("id", "in", self.mapped("picking_ids").ids)],
                safe_eval(action.domain or "[]"),
            ]
        )
        action_dict["context"] = safe_eval(
            action_dict.get("context", "{}"))
        action_dict["context"].update({
            "default_task_id": self.id,
            "default_analytic_account_id": self.project_id.analytic_account_id.id,
        })
        action_dict.update({"domain": domain})
        return action_dict
