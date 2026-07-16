# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, fields, models


class ReportLineagePercentageXlsx(models.AbstractModel):
    _name = "report.lineage_percentage_xlsx"
    _inherit = "report.report_xlsx.abstract"
    _description = "Lineage Percentage Report"

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
        int_format = workbook.add_format(
            {
                "num_format": "#,##0;(#,##0)",
            }
        )
        two_decimal_format = workbook.add_format(
            {
                "num_format": "#,##0.00;(#,##0.00)",
            }
        )
        three_decimal_format = workbook.add_format(
            {
                "num_format": "#,##0.000;(#,##0.000)",
            }
        )
        eight_decimal_format = workbook.add_format(
            {
                "num_format": "#,##0.00000000;(#,##0.0000000000)",
            }
        )
        table_header.set_text_wrap()
        int_format.set_text_wrap()
        two_decimal_format.set_text_wrap()
        three_decimal_format.set_text_wrap()
        eight_decimal_format.set_text_wrap()
        table_detail_right_num = workbook.add_format(
            {
                "border": 1,
                "align": "right",
                "valign": "vcenter",
            }
        )
        table_detail_right_num.set_num_format("#,##0.00")
        n = 1
        worksheet = workbook.add_worksheet("Breeding Report By Mother")
        for i in range(0, 28):
            worksheet.set_column(0, i, 12)
        worksheet.write(0, 0, _("Breeding"), table_header)
        worksheet.write(0, 1, _("Lineage"), table_header)
        worksheet.write(0, 2, _("Lineage %"), table_header)
        worksheet.write(0, 3, _("Entry Date"), table_header)
        worksheet.write(0, 4, _("Cleaned Date"), table_header)
        worksheet.write(0, 5, _("Farm"), table_header)
        worksheet.write(0, 6, _("City"), table_header)
        worksheet.write(0, 7, _("Entry Qty"), table_header)
        worksheet.write(0, 8, _("Output Qty"), table_header)
        worksheet.write(0, 9, _("Cancellation %"), table_header)
        worksheet.write(0, 10, _("Density"), table_header)
        worksheet.write(0, 11, _("Growth Speed"), table_header)
        worksheet.write(0, 12, _("FEEP"), table_header)
        worksheet.write(0, 13, _("Meat Kilos"), table_header)
        worksheet.write(0, 14, _("Output Amount"), table_header)
        worksheet.write(0, 15, _("Consume Feed"), table_header)
        worksheet.write(0, 16, _("Feed Amount"), table_header)
        worksheet.write(0, 17, _("Feed Family"), table_header)
        worksheet.write(0, 18, _("Medicine Amount"), table_header)
        worksheet.write(0, 19, _("Average Age"), table_header)
        worksheet.write(0, 20, _("Farm Day"), table_header)
        worksheet.write(0, 21, _("Average Weight"), table_header)
        worksheet.write(0, 22, _("Conversion"), table_header)
        worksheet.write(0, 23, _("Dif."), table_header)
        worksheet.write(0, 24, _("Liquidation Amount"), table_header)
        worksheet.write(0, 25, _("Chick Liquidation"), table_header)
        worksheet.write(0, 26, _("Liquidation Area"), table_header)
        worksheet.write(0, 27, _("Cost Kilo"), table_header)
        for line in objects:
            worksheet.write(n, 0, line.batch_id.name if line.batch_id else "")
            worksheet.write(n, 1, line.lineage_id.name if line.lineage_id else "")
            worksheet.write(n, 2, round(line.percentage, 3), three_decimal_format)
            worksheet.write(
                n,
                3,
                fields.Date.from_string(line.entry_date).strftime("%d-%m-%Y")
                if line.entry_date
                else "",
            )
            worksheet.write(
                n,
                4,
                fields.Date.from_string(line.cleaned_date).strftime("%d-%m-%Y")
                if line.cleaned_date
                else "",
            )
            worksheet.write(n, 5, line.warehouse_id.name if line.warehouse_id else "")
            worksheet.write(n, 6, line.city if line.city else "")
            worksheet.write(n, 7, line.chick_entry_qty, int_format)
            worksheet.write(n, 8, line.output_units, int_format)
            worksheet.write(
                n, 9, round(line.cancellation_percentage, 2), two_decimal_format
            )
            worksheet.write(n, 10, round(line.density, 2), two_decimal_format)
            worksheet.write(n, 11, round(line.growth_speed, 2), two_decimal_format)
            worksheet.write(n, 12, line.feed, int_format)
            worksheet.write(n, 13, line.meat_kilos, int_format)
            worksheet.write(
                n, 14, round(line.output_amount_days, 2), two_decimal_format
            )
            worksheet.write(n, 15, line.consume_feed, int_format)
            worksheet.write(
                n, 16, round(line.output_feed_amount, 2), two_decimal_format
            )
            worksheet.write(n, 17, line.feed_family.name if line.feed_family else "")
            worksheet.write(n, 18, round(line.medicine_amount, 2), two_decimal_format)
            worksheet.write(n, 19, round(line.average_age, 2), two_decimal_format)
            worksheet.write(n, 20, line.farm_day, int_format)
            worksheet.write(n, 21, round(line.average_weight, 3), three_decimal_format)
            worksheet.write(n, 22, round(line.conversion, 3), three_decimal_format)
            worksheet.write(n, 23, round(line.dif_weight, 3), three_decimal_format)
            worksheet.write(
                n, 24, round(line.liquidation_amount, 2), two_decimal_format
            )
            worksheet.write(
                n, 25, round(line.chick_liquidation, 8), eight_decimal_format
            )
            worksheet.write(
                n, 26, round(line.liquidation_area, 8), eight_decimal_format
            )
            worksheet.write(n, 27, round(line.cost_kilo, 3), three_decimal_format)
            n = n + 1
        worksheet.write(n, 7, sum(objects.mapped("chick_entry_qty")), int_format)
        worksheet.write(n, 8, sum(objects.mapped("output_units")), int_format)
        cancellation = (
            (
                sum(objects.mapped("chick_entry_qty"))
                - sum(objects.mapped("output_units"))
            )
            * 100
            / sum(objects.mapped("chick_entry_qty"))
            if sum(objects.mapped("chick_entry_qty"))
            else 0
        )
        worksheet.write(n, 9, round(cancellation, 2), two_decimal_format)
        density = sum(objects.mapped("chick_entry_qty")) / sum(
            objects.mapped("warehouse_area")
        )
        worksheet.write(n, 10, round(density, 2), two_decimal_format)
        average_age = (
            sum(objects.mapped("age_output")) / sum(objects.mapped("output_units"))
            if sum(objects.mapped("output_units"))
            else 0
        )
        growth_speed = (
            sum(objects.mapped("meat_kilos"))
            / sum(objects.mapped("output_units"))
            / average_age
            * 1000
            if sum(objects.mapped("output_units")) and average_age
            else 0
        )
        worksheet.write(n, 11, round(growth_speed, 2), two_decimal_format)
        conversion = (
            sum(objects.mapped("consume_feed")) / sum(objects.mapped("meat_kilos"))
            if sum(objects.mapped("meat_kilos"))
            else 0
        )
        feep = (
            growth_speed * (100 - cancellation) / (10 * conversion)
            if conversion != 0
            else 0
        )
        worksheet.write(n, 12, int(feep), int_format)
        worksheet.write(n, 13, sum(objects.mapped("meat_kilos")), int_format)
        worksheet.write(
            n,
            14,
            round(sum(objects.mapped("output_amount_days")), 2),
            two_decimal_format,
        )
        worksheet.write(n, 15, sum(objects.mapped("consume_feed")), int_format)
        worksheet.write(
            n,
            16,
            round(sum(objects.mapped("output_feed_amount")), 2),
            two_decimal_format,
        )
        worksheet.write(
            n, 18, round(sum(objects.mapped("medicine_amount")), 2), two_decimal_format
        )
        worksheet.write(n, 19, round(average_age, 2), two_decimal_format)
        worksheet.write(
            n, 20, int(sum(objects.mapped("farm_day")) / (n - 1)), int_format
        )
        average_weight = (
            sum(objects.mapped("meat_kilos")) / sum(objects.mapped("output_units"))
            if sum(objects.mapped("output_units"))
            else 0
        )
        worksheet.write(n, 21, round(average_weight, 3), three_decimal_format)
        worksheet.write(n, 22, round(conversion, 3), three_decimal_format)
        worksheet.write(
            n, 23, round(average_weight - conversion, 3), three_decimal_format
        )
        worksheet.write(
            n,
            24,
            round(sum(objects.mapped("liquidation_amount")), 2),
            two_decimal_format,
        )
        worksheet.write(
            n,
            25,
            round(
                sum(objects.mapped("liquidation_amount"))
                / sum(objects.mapped("output_units")),
                8,
            ),
            eight_decimal_format,
        )
        worksheet.write(
            n,
            26,
            round(
                sum(objects.mapped("liquidation_amount"))
                / sum(objects.mapped("warehouse_area")),
                8,
            ),
            eight_decimal_format,
        )
        worksheet.write(
            n,
            27,
            round(
                sum(objects.mapped("liquidation_amount"))
                / sum(objects.mapped("meat_kilos")),
                3,
            ),
            three_decimal_format,
        )
