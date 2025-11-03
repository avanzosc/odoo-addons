# Copyright 2025 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class AccountAnalyticAccount(models.Model):
    _inherit = "account.analytic.account"

    sale_order_count = fields.Integer(
        string="# Sale orders", compute="_compute_sale_order_count"
    )

    def _compute_sale_order_count(self):
        for account in self:
            cond = [("analytic_account_id", "=", account.id)]
            sales = self.env["sale.order"].search(cond)
            account.sale_order_count = len(sales)

    def action_view_sale_orders_from_analytic(self):
        self.ensure_one()
        cond = [("analytic_account_id", "=", self.id)]
        sales = self.env["sale.order"].search(cond)
        action = self.env["ir.actions.actions"]._for_xml_id("sale.action_orders")
        action["domain"] = [("id", "in", sales.ids)]
        return action
