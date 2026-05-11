# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, models


class ProductConsumptionXlsx(models.AbstractModel):
    _name = "report.product_consumption_xlsx"
    _inherit = "report.report_xlsx.abstract"
    _description = "Abstract model to export as xlsx the product consumption"

    def generate_xlsx_report(self, workbook, data, objects):
        table_header = workbook.add_format(
            {
                "bold": True,
                "border": 1,
                "align": "center",
                "valign": "vcenter",
                "fg_color": "#D7E4BC",
            }
        )
        table = workbook.add_format(
            {
                "bold": True,
                "border": 1,
                "align": "center",
                "valign": "vcenter",
            }
        )
        table_header.set_text_wrap()
        table.set_text_wrap()
        table_detail_right_num = workbook.add_format(
            {
                "border": 1,
                "align": "right",
                "valign": "vcenter",
            }
        )
        table_detail_right_num.set_num_format("#,##0.00")
        worksheet = workbook.add_worksheet("Product Consumption")
        n = 0
        worksheet.set_row(n, 45)
        for i in range(0, 14):
            worksheet.set_column(0, i, 25)
        location = self.env["stock.location"].browse(data.get("location"))
        worksheet.write(n, 0, location.name, table_header)
        worksheet.write(n, 1, data["date_start"], table_header)
        worksheet.write(n, 3, data["date_end"], table_header)
        n += 1
        worksheet.write(n, 0, _("Product"), table_header)
        worksheet.write(n, 1, _("Initial Inventory"), table_header)
        worksheet.write(n, 2, _("Entries"), table_header)
        worksheet.write(n, 3, _("Final Inventory"), table_header)
        worksheet.write(n, 4, _("Consumption"), table_header)
        worksheet.write(n, 5, _("Cost Unit"), table_header)
        worksheet.write(n, 6, _("Total"), table_header)
        worksheet.write(n, 7, _("End Inventory Value"), table_header)
        variants = self.env["product.product"].browse(data.get("product_variants"))
        for product in variants:
            n += 1
            qty_date_start = product.with_context(
                to_date=data["date_start"],
                location=location.id,
            ).qty_available
            qty_date_end = product.with_context(
                to_date=data["date_end"],
                location=location.id,
            ).qty_available
            entry_lines = self.env["stock.move.line"].search(
                [
                    ("product_id", "=", product.id),
                    ("location_dest_id", "=", location.id),
                    ("picking_code", "=", "incoming"),
                    ("date", ">=", data["date_start"]),
                    ("date", "<=", data["date_end"]),
                    ("state", "=", "done"),
                ]
            )
            entry_qty = sum(entry_lines.mapped("qty_done"))
            consumption = qty_date_start + entry_qty - qty_date_end
            worksheet.write(n, 0, product.display_name, table)
            worksheet.write(n, 1, qty_date_start, table)
            worksheet.write(n, 2, entry_qty, table)
            worksheet.write(n, 3, qty_date_end, table)
            worksheet.write(n, 4, consumption, table)
            worksheet.write(n, 5, product.last_purchase_price, table)
            worksheet.write(n, 6, product.last_purchase_price * consumption, table)
            worksheet.write(n, 7, product.last_purchase_price * qty_date_end, table)
