# Copyright 2026 Ane Gurruchaga - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class TreasuryForecastSaleOrderWizard(models.TransientModel):
    _name = "treasury.forecast.sale.order.wizard"
    _description = "Create Sales Quotation from Treasury Forecast"

    forecast_line_ids = fields.Many2many(
        comodel_name="treasury.forecast",
        string="Treasury Forecast Lines",
        readonly=True,
    )
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Partner Project",
    )

    @api.model
    def default_get(self, fields_list):
        values = super().default_get(fields_list)
        lines = (
            self.env["treasury.forecast"]
            .browse(self.env.context.get("active_ids", []))
            .exists()
        )
        project = lines._get_sale_order_project()
        values.update(
            {
                "forecast_line_ids": [(6, 0, lines.ids)],
                "partner_id": project.partner_id.id,
            }
        )
        return values

    def button_create_sale_order(self):
        self.ensure_one()
        return self.forecast_line_ids.action_create_sale_order(self.partner_id)
