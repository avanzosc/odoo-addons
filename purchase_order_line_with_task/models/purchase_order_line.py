# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    allowed_task_ids = fields.Many2many(
        string="Allowed tasks",
        comodel_name="project.task",
        compute="_compute_allowed_task_ids")
    task_id = fields.Many2one(
        string="Task", comodel_name="project.task")

    @api.depends("account_analytic_id",
                 "account_analytic_id.project_ids",
                 "account_analytic_id.project_ids.task_ids")
    def _compute_allowed_task_ids(self):
        for line in self:
            line.allowed_task_ids = [
                (6, 0, line.mapped(
                    "account_analytic_id.project_ids.task_ids").ids)]

    @api.onchange("account_analytic_id")
    def onchange_account_analytic_id(self):
        for line in self:
            if line.task_id and line.task_id not in line.allowed_task_ids:
                line.task_id = False
            elif len(line.allowed_task_ids) == 1:
                line.task_id = line.allowed_task_ids[:1]
