# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import base64
import io

import xlsxwriter

from odoo import fields, models


class ProductCatalogWeb(models.Model):
    _name = "product.catalog.web"
    _description = "Product Catalog Web"

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
    logo = fields.Binary()
    description = fields.Text(translate=True)
    inventory_availability = fields.Selection(
        selection=[
            ("never", "Never"),
            ("always", "Always"),
            ("threshold", "On Threshold"),
            ("custom", "Custom"),
        ],
    )
    visible_slider = fields.Boolean(string="Visible on Website", default=True)
    company_id = fields.Many2one(
        comodel_name="res.company",
        required=True,
        default=lambda self: self.env.company,
    )
    warehouse_id = fields.Many2one(
        comodel_name="stock.warehouse",
        required=True,
        default=lambda self: self.env["stock.warehouse"].search(
            [("company_id", "=", self.env.company.id)], limit=1
        ),
    )
    product_ids = fields.Many2many(
        comodel_name="product.template",
        relation="catalog_web_product_template_rel",
        column1="catalog_id",
        column2="product_tmpl_id",
        string="Products",
    )

    def action_export(self):
        self.ensure_one()
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {"in_memory": True})
        worksheet = workbook.add_worksheet("Productos")

        header_fmt = workbook.add_format(
            {"bold": True, "border": 1, "align": "center", "fg_color": "#D7E4BC"}
        )
        cell_fmt = workbook.add_format({"border": 1})

        worksheet.set_column(0, 0, 20)
        worksheet.set_column(1, 1, 50)

        worksheet.write(0, 0, "Internal Reference", header_fmt)
        worksheet.write(0, 1, "Name", header_fmt)

        for row, product in enumerate(self.product_ids, start=1):
            worksheet.write(row, 0, product.default_code or "", cell_fmt)
            worksheet.write(row, 1, product.name or "", cell_fmt)

        workbook.close()
        output.seek(0)

        filename = f"{self.name}_productos.xlsx".replace(" ", "_")
        attachment = self.env["ir.attachment"].create(
            {
                "name": filename,
                "datas": base64.encodebytes(output.read()),
                "res_model": self._name,
                "res_id": self.id,
                "type": "binary",
            }
        )
        return {
            "type": "ir.actions.act_url",
            "url": f"/web/content/{attachment.id}?download=true",
            "target": "self",
        }
