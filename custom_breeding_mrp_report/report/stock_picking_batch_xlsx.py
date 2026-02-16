# Copyright 2025 Lucía Echeverría - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import _, models


class ReportStockPickingBatchXlsx(models.AbstractModel):
    _inherit = "report.stock_picking_batch_xlsx"

    def generate_xlsx_report(self, workbook, data, objects):
        super().generate_xlsx_report(workbook, data, objects)
        table_header = workbook.add_format(
            {
                "bold": True,
                "border": 1,
                "align": "center",
                "valign": "vcenter",
                "fg_color": "#D7E4BC",
            }
        )
        table_header.set_text_wrap()
        two_decimal_format = workbook.add_format(
            {
                "num_format": "#,##0.00;(#,##0.00)",
            }
        )
        two_decimal_format.set_text_wrap()
        worksheet = workbook.get_worksheet_by_name("Breeding Report")
        worksheet.write(0, 29, _("Seized %"), table_header)
        n = 1
        for line in objects:
            worksheet.write(n, 29, round(line.seized_percentage, 2), two_decimal_format)
            n += 1
        seized_percentage = (
            (sum(objects.mapped("seized_units")) / sum(objects.mapped("output_units")))
            * 100
            if sum(objects.mapped("output_units"))
            else 0
        )
        worksheet.write(n, 29, round(seized_percentage, 2), two_decimal_format)
