# Copyright 2025 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProductConsumptionWizard(models.TransientModel):
    _name = "product.consumption.wizard"
    _description = "Wizard to generate a report with the sonsuption of the products"

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
        data = {}
        location = self.location_id
        date_start = self.date_start
        date_end = self.date_end
        data.update(
            {"date_start": date_start, "date_end": date_end, "location": location.id}
        )
        products_tmpl = self.env["product.template"]._context.get("active_ids")
        products_tmpl = self.env["product.template"].browse(products_tmpl)
        product_variants = []
        for tmpl in products_tmpl:
            product_var = self.env["product.product"].search(
                [("product_tmpl_id", "=", tmpl.id)]
            )
            product_variants.append(product_var.id)
        data.update({"product_variants": product_variants})
        return self.env.ref(
            "product_consumption_report.report_product_consumption_xlsx"
        ).report_action(self, data=data)
