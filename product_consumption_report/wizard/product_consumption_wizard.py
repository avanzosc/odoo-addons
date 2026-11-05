# Copyright 2025 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models
from odoo.tools.misc import format_datetime


class ProductConsumptionWizard(models.TransientModel):
    _name = "product.consumption.wizard"
    _description = "Wizard to generate a product consumption report"

    location_id = fields.Many2one(
        string="Location",
        comodel_name="stock.location",
        required=True,
        domain="[('usage', '=', 'internal')]",
    )
    date_start = fields.Datetime(required=True)
    date_end = fields.Datetime(required=True)

    def button_generate_report(self):
        self.ensure_one()
        products_tmpl = self.env["product.template"].browse(
            self.env.context.get("active_ids", [])
        )
        data = {
            "date_start": fields.Datetime.to_string(self.date_start),
            "date_end": fields.Datetime.to_string(self.date_end),
            "date_start_display": format_datetime(
                self.env,
                self.date_start,
                tz=self.env.context.get("tz"),
                dt_format=False,
            ),
            "date_end_display": format_datetime(
                self.env,
                self.date_end,
                tz=self.env.context.get("tz"),
                dt_format=False,
            ),
            "location": self.location_id.id,
            "product_variants": products_tmpl.product_variant_ids.ids,
        }
        return self.env.ref(
            "product_consumption_report.report_product_consumption_xlsx"
        ).report_action(self, data=data)
