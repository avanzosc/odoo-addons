# Copyright 2026 Ane Gurruchaga - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from collections import defaultdict

from odoo import _, fields, models
from odoo.exceptions import UserError


class TreasuryForecast(models.Model):
    _inherit = "treasury.forecast"

    purchase_line_id = fields.Many2one(
        comodel_name="purchase.order.line",
        string="Purchase Order Line",
        copy=False,
        readonly=True,
        index=True,
    )

    def _get_purchase_cost_lines(self):
        cost_lines = self.filtered(lambda line: line.expense > 0)
        if any(not line.partner_id for line in cost_lines):
            raise UserError(_("All cost lines must have a supplier assigned."))
        return cost_lines

    def action_create_purchase_orders(self):
        cost_lines = self._get_purchase_cost_lines()
        lines_by_supplier = defaultdict(lambda: self.env["treasury.forecast"])
        for line in cost_lines:
            lines_by_supplier[line.partner_id] |= line

        orders = self.env["purchase.order"]
        for supplier, forecast_lines in lines_by_supplier.items():
            order = self.env["purchase.order"].create(
                {
                    "partner_id": supplier.id,
                }
            )
            orders |= order
            for forecast_line in forecast_lines:
                purchase_line = self.env["purchase.order.line"].create(
                    {
                        "order_id": order.id,
                        "product_id": forecast_line.product_id.id,
                        "product_qty": forecast_line.quantity,
                        "price_unit": forecast_line.expense_price,
                        "project_id": forecast_line.project_id.id,
                    }
                )
                forecast_line.purchase_line_id = purchase_line

        action = self.env["ir.actions.actions"]._for_xml_id("purchase.purchase_rfq")
        action["domain"] = [("id", "in", orders.ids)]
        if len(orders) == 1:
            action.update(
                {
                    "res_id": orders.id,
                    "views": [
                        (self.env.ref("purchase.purchase_order_form").id, "form")
                    ],
                }
            )
        return action
