# Copyright 2026 Ane Gurruchaga - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class TreasuryForecastPurchaseOrderWizard(models.TransientModel):
    _name = "treasury.forecast.purchase.order.wizard"
    _description = "Create Purchase Quotations from Treasury Forecast"

    forecast_line_ids = fields.Many2many(
        comodel_name="treasury.forecast",
        string="Treasury Forecast Lines",
        readonly=True,
    )

    @api.model
    def default_get(self, fields_list):
        values = super().default_get(fields_list)
        lines = (
            self.env["treasury.forecast"]
            .browse(self.env.context.get("active_ids", []))
            .exists()
        )
        lines._get_purchase_cost_lines()
        values["forecast_line_ids"] = [(6, 0, lines.ids)]
        return values

    def button_create_purchase_orders(self):
        self.ensure_one()
        return self.forecast_line_ids.action_create_purchase_orders()
