# Copyright 2019 Alejandro Nieto - Okatent
# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    analytic_account_id = fields.Many2one(
        string="Project", comodel_name="account.analytic.account"
    )

    @api.onchange("analytic_account_id")
    def _onchange_analytic_account_id(self):
        for order in self:
            if not order.analytic_account_id:
                order.order_line.analytic_distribution = False
                order.project_id = False
                continue
            analytic_distribution = {str(order.analytic_account_id.id): 100.0}
            order.order_line.analytic_distribution = analytic_distribution
            if (
                "from_change_project" not in self.env.context
                and len(order.analytic_account_id.project_ids) == 1
            ):
                order.with_context(
                    from_change_analytic_account=True
                ).project_id = order.analytic_account_id.project_ids[0].id

    @api.onchange("project_id")
    def _onchange_project_id_(self):
        if "from_change_analytic_account" not in self.env.context:
            for order in self:
                if order.project_id.account_id:
                    order.with_context(
                        from_change_project=True
                    ).analytic_account_id = order.project_id.account_id.id
