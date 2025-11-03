# Copyright 2025 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class ProjectProject(models.Model):
    _inherit = "project.project"

    count_sale_order = fields.Integer(
        string="# Sale orders",
        compute="_compute_count_sale_order",
    )

    def _compute_count_sale_order(self):
        for project in self:
            cond = [("analytic_account_id", "=", project.analytic_account_id.id)]
            sales = self.env["sale.order"].search(cond)
            project.count_sale_order = len(sales)

    def action_view_sale_orders_from_project(self):
        self.ensure_one()
        cond = [("analytic_account_id", "=", self.analytic_account_id.id)]
        sales = self.env["sale.order"].search(cond)
        action = self.env["ir.actions.actions"]._for_xml_id("sale.action_orders")
        action["domain"] = [("id", "in", sales.ids)]
        return action
