# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, models


class ReportBreedingGeneralSummaryXlsx(models.AbstractModel):
    _name = "report.breeding_general_summary_xlsx"
    _inherit = "report.report_xlsx.abstract"
    _description = "Breeding General Summary Report"

    def generate_xlsx_report(self, workbook, data, objects):
        table_header = workbook.add_format(
            {
                "bold": True,
                "align": "center",
                "valign": "vcenter",
                "fg_color": "#D7E4BC",
            }
        )
        summary = workbook.add_format(
            {
                "bold": True,
                "num_format": "#,##0.00;(#,##0.00)",
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
                "num_format": "#,##0.00000000;(#,##0.00000000)",
            }
        )
        result_two_decimal = workbook.add_format(
            {
                "fg_color": "#afd095",
                "num_format": "#,##0.00;(#,##0.00)",
            }
        )
        result_three_decimal = workbook.add_format(
            {
                "fg_color": "#afd095",
                "num_format": "#,##0.000;(#,##0.000)",
            }
        )
        result_summary = workbook.add_format(
            {
                "bold": True,
                "fg_color": "#afd095",
                "num_format": "#,##0.000;(#,##0.000)",
            }
        )
        table_header.set_text_wrap()
        summary.set_text_wrap()
        int_format.set_text_wrap()
        two_decimal_format.set_text_wrap()
        three_decimal_format.set_text_wrap()
        eight_decimal_format.set_text_wrap()
        result_three_decimal.set_text_wrap()
        result_two_decimal.set_text_wrap()
        result_summary.set_text_wrap()
        table_detail_right_num = workbook.add_format(
            {
                "border": 1,
                "align": "right",
                "valign": "vcenter",
            }
        )
        table_detail_right_num.set_num_format("#,##0.00")
        worksheet = workbook.add_worksheet("Breeding General Summary")
        for i in range(0, 9):
            worksheet.set_column(0, i, 20)
        n = 0
        m = 0
        worksheet.write(n, m, _("Concept"), table_header)
        m += 1
        worksheet.write(n, m, _("Value"), table_header)
        m += 1
        worksheet.write(n, m, _("Units"), table_header)
        m += 1
        worksheet.write(n, m, _("%"), table_header)
        m += 1
        worksheet.write(n, m, _("Kg"), table_header)
        m += 1
        worksheet.write(n, m, _("Price"), table_header)
        m += 1
        worksheet.write(n, m, _("Amount"), table_header)
        m += 1
        worksheet.write(n, m, _("Per Kilo"), table_header)
        m += 1
        worksheet.write(n, m, _("Per Chick"), table_header)
        n += 2
        m = 0
        worksheet.write(n, m, _("Movement Summary"), table_header)
        for m in range(m + 1, 9):
            worksheet.write(n, m, "", table_header)
        n += 1
        m = 0
        worksheet.write(n, m, _("Chick Input"))
        m += 2
        chick_qty = sum(objects.mapped("chick_entry_qty"))
        worksheet.write(n, m, chick_qty, int_format)
        m += 1
        worksheet.write(n, m, 100, two_decimal_format)
        m += 2
        entry_chicken_amount = sum(objects.mapped("entry_chicken_amount"))
        unit = entry_chicken_amount / chick_qty if chick_qty else 0
        worksheet.write(n, m, round(unit, 8), eight_decimal_format)
        m += 1
        worksheet.write(n, m, round(entry_chicken_amount, 2), two_decimal_format)
        m += 1
        meat_kilos = sum(objects.mapped("meat_kilos"))
        unit = entry_chicken_amount / meat_kilos if meat_kilos else 0
        worksheet.write(n, m, round(unit, 3), three_decimal_format)
        m += 1
        output_unit = sum(objects.mapped("output_units"))
        unit = entry_chicken_amount / output_unit if output_unit else 0
        worksheet.write(n, m, round(unit, 3), three_decimal_format)
        n += 1
        m = 0
        worksheet.write(n, m, _("Chicken Output"))
        m += 2
        worksheet.write(n, m, output_unit, int_format)
        m += 1
        percentage = output_unit * 100 / chick_qty if chick_qty else 0
        worksheet.write(n, m, round(percentage, 2), two_decimal_format)
        m += 1
        worksheet.write(n, m, meat_kilos, int_format)
        m += 1
        output_amount = sum(objects.mapped("output_amount"))
        unit = output_amount / meat_kilos if meat_kilos else 0
        worksheet.write(n, m, round(unit, 8), eight_decimal_format)
        m += 1
        worksheet.write(n, m, round(output_amount, 2), two_decimal_format)
        m += 1
        unit = output_amount / meat_kilos if meat_kilos else 0
        worksheet.write(n, m, round(unit, 3), three_decimal_format)
        m += 1
        unit = output_amount / output_unit if output_unit else 0
        worksheet.write(n, m, round(unit, 3), three_decimal_format)
        n += 1
        m = 0
        worksheet.write(n, m, _("Total Cancellations"))
        m += 2
        worksheet.write(n, m, chick_qty - output_unit, int_format)
        m += 1
        cancellation_percentage = (
            100 - output_unit * 100 / chick_qty if chick_qty else 0
        )
        worksheet.write(n, m, round(cancellation_percentage, 2), two_decimal_format)
        n += 1
        m = 0
        worksheet.write(n, m, _("Consumed Feed"))
        m += 4
        feed_qty = sum(objects.mapped("consume_feed"))
        worksheet.write(n, m, feed_qty, int_format)
        feed_amount = sum(objects.mapped("output_feed_amount"))
        m += 1
        unit = feed_amount / feed_qty if feed_qty else 0
        worksheet.write(n, m, round(unit, 8), eight_decimal_format)
        m += 1
        worksheet.write(n, m, round(feed_amount, 2), two_decimal_format)
        n += 1
        m = 0
        worksheet.write(n, m, _("Medicine"))
        m += 2
        medicine_qty = sum(objects.mapped("medicine_qty"))
        output_medicine_amount = sum(objects.mapped("output_medicine_amount"))
        worksheet.write(n, m, medicine_qty, int_format)
        m += 3
        unit = output_medicine_amount / medicine_qty if medicine_qty else 0
        worksheet.write(n, m, round(unit, 8), eight_decimal_format)
        m += 1
        worksheet.write(n, m, round(output_medicine_amount, 2), two_decimal_format)
        m += 1
        unit = output_medicine_amount / meat_kilos if meat_kilos else 0
        worksheet.write(n, m, round(unit, 3), three_decimal_format)
        m += 1
        unit = output_medicine_amount / output_unit if output_unit else 0
        worksheet.write(n, m, round(unit, 3), three_decimal_format)
        n += 1
        m = 0
        worksheet.write(n, m, _("Liquidation"))
        m += 2
        worksheet.write(n, m, output_unit, int_format)
        m += 2
        worksheet.write(n, m, meat_kilos, int_format)
        m += 2
        liquidation_amount = sum(objects.mapped("liquidation_amount"))
        worksheet.write(n, m, round(liquidation_amount, 2), two_decimal_format)
        m += 1
        unit = liquidation_amount / meat_kilos if meat_kilos else 0
        worksheet.write(n, m, round(unit, 3), three_decimal_format)
        m += 1
        unit = liquidation_amount / output_unit if output_unit else 0
        worksheet.write(n, m, round(unit, 3), three_decimal_format)
        n += 2
        m = 0
        worksheet.write(n, m, _("Costs and Benefits"), table_header)
        for m in range(m + 1, 9):
            worksheet.write(n, m, "", table_header)
        n += 1
        m = 0
        chick_amount = 0
        feed_amount = 0
        medicine_amount = 0
        liquidation_amount = 0
        chicken_load = 0
        overheads = 0
        sales = 0
        total_costs = 0
        for line in objects:
            chick = (-1) * sum(
                line.analytic_line_ids.filtered(lambda c: c.name == "Pollito").mapped(
                    "amount"
                )
            )
            chick_amount += chick
            feed = (-1) * sum(
                line.analytic_line_ids.filtered(lambda c: c.name == "Pienso").mapped(
                    "amount"
                )
            )
            feed_amount += feed
            medicine = (-1) * sum(
                line.analytic_line_ids.filtered(
                    lambda c: c.name == "Medicamento"
                ).mapped("amount")
            )
            medicine_amount += medicine
            liquidation = (-1) * sum(
                line.analytic_line_ids.filtered(
                    lambda c: c.name == "Liquidación"
                ).mapped("amount")
            )
            liquidation_amount += liquidation
            load = (-1) * sum(
                line.analytic_line_ids.filtered(
                    lambda c: c.name == "Carga Pollos"
                ).mapped("amount")
            )
            chicken_load += load
            expenses = (-1) * sum(
                line.analytic_line_ids.filtered(
                    lambda c: c.name == "Gtos. Generales"
                ).mapped("amount")
            )
            overheads += expenses
            sales += sum(
                line.analytic_line_ids.filtered(lambda c: c.name == "Ventas").mapped(
                    "amount"
                )
            )
            total_costs += chick + feed + medicine + liquidation + load + expenses
        worksheet.write(n, m, _("Chicks"))
        m += 3
        unit = chick_amount * 100 / total_costs if total_costs else 0
        worksheet.write(n, m, round(unit, 2), result_two_decimal)
        m += 3
        worksheet.write(n, m, round(chick_amount, 2), two_decimal_format)
        m += 1
        unit = chick_amount / meat_kilos if meat_kilos else 0
        worksheet.write(n, m, round(unit, 3), result_three_decimal)
        m += 1
        unit = chick_amount / output_unit if output_unit else 0
        worksheet.write(n, m, round(unit, 3), result_three_decimal)
        n += 1
        m = 0
        worksheet.write(n, m, _("Feed"))
        m += 3
        unit = feed_amount * 100 / total_costs if total_costs else 0
        worksheet.write(n, m, round(unit, 2), result_two_decimal)
        m += 3
        worksheet.write(n, m, round(feed_amount, 2), two_decimal_format)
        m += 1
        unit = feed_amount / meat_kilos if meat_kilos else 0
        worksheet.write(n, m, round(unit, 3), result_three_decimal)
        m += 1
        unit = feed_amount / output_unit if output_unit else 0
        worksheet.write(n, m, round(unit, 3), result_three_decimal)
        n += 1
        m = 0
        worksheet.write(n, m, _("Medicine"))
        m += 3
        unit = medicine_amount * 100 / total_costs if total_costs else 0
        worksheet.write(n, m, round(unit, 2), result_two_decimal)
        m += 3
        worksheet.write(n, m, round(medicine_amount, 2), two_decimal_format)
        m += 1
        unit = medicine_amount / meat_kilos if meat_kilos else 0
        worksheet.write(n, m, round(unit, 3), result_three_decimal)
        m += 1
        unit = medicine_amount / output_unit if output_unit else 0
        worksheet.write(n, m, round(unit, 3), result_three_decimal)
        n += 1
        m = 0
        worksheet.write(n, m, _("Liquidation"))
        m += 3
        unit = liquidation_amount * 100 / total_costs if total_costs else 0
        worksheet.write(n, m, round(unit, 2), result_two_decimal)
        m += 3
        worksheet.write(n, m, round(liquidation_amount, 2), two_decimal_format)
        m += 1
        unit = liquidation_amount / meat_kilos if meat_kilos else 0
        worksheet.write(n, m, round(unit, 3), result_three_decimal)
        m += 1
        unit = liquidation_amount / output_unit if output_unit else 0
        worksheet.write(n, m, round(unit, 3), result_three_decimal)
        n += 1
        m = 0
        worksheet.write(n, m, _("Chicken Load"))
        m += 3
        unit = chicken_load * 100 / total_costs if total_costs else 0
        worksheet.write(n, m, round(unit, 2), result_two_decimal)
        m += 3
        worksheet.write(n, m, round(chicken_load, 2), two_decimal_format)
        m += 1
        unit = chicken_load / meat_kilos if meat_kilos else 0
        worksheet.write(n, m, round(unit, 3), result_three_decimal)
        m += 1
        unit = chicken_load / output_unit if output_unit else 0
        worksheet.write(n, m, round(unit, 3), result_three_decimal)
        n += 1
        m = 0
        worksheet.write(n, m, _("Overheads"))
        m += 3
        unit = overheads * 100 / total_costs if total_costs else 0
        worksheet.write(n, m, round(unit, 2), result_two_decimal)
        m += 3
        worksheet.write(n, m, round(overheads, 2), two_decimal_format)
        m += 1
        unit = overheads / meat_kilos if meat_kilos else 0
        worksheet.write(n, m, round(unit, 3), result_three_decimal)
        m += 1
        unit = overheads / output_unit if output_unit else 0
        worksheet.write(n, m, round(unit, 3), result_three_decimal)
        n += 1
        m = 0
        worksheet.write(n, m, _("Total Costs"), summary)
        m += 6
        worksheet.write(n, m, round(total_costs, 2), summary)
        m += 1
        unit = total_costs / meat_kilos if meat_kilos else 0
        worksheet.write(n, m, round(unit, 3), result_summary)
        m += 1
        unit = total_costs / output_unit if output_unit else 0
        worksheet.write(n, m, round(unit, 3), result_summary)
        n += 1
        m = 0
        worksheet.write(n, m, _("Total Sales"), summary)
        m += 6
        worksheet.write(n, m, round(sales, 2), summary)
        m += 1
        unit = sales / meat_kilos if meat_kilos else 0
        worksheet.write(n, m, round(unit, 3), result_summary)
        m += 1
        unit = sales / output_unit if output_unit else 0
        worksheet.write(n, m, round(unit, 3), result_summary)
        n += 1
        m = 0
        worksheet.write(n, m, _("Loss/Benefits"), summary)
        m += 6
        benefits = sales - total_costs
        worksheet.write(n, m, round(benefits, 2), summary)
        m += 1
        unit = benefits / meat_kilos if meat_kilos else 0
        worksheet.write(n, m, round(unit, 3), result_summary)
        m += 1
        unit = benefits / output_unit if output_unit else 0
        worksheet.write(n, m, round(unit, 3), result_summary)
        n += 2
        m = 0
        worksheet.write(n, m, _("Results"), table_header)
        for m in range(m + 1, 9):
            worksheet.write(n, m, "", table_header)
        n += 1
        m = 0
        worksheet.write(n, m, _("Cancellation %"))
        m += 1
        worksheet.write(n, m, round(cancellation_percentage, 2), two_decimal_format)
        n += 1
        m = 0
        worksheet.write(n, m, _("Total M2"))
        m += 1
        area = sum(objects.mapped("warehouse_area"))
        worksheet.write(n, m, area, int_format)
        n += 1
        m = 0
        worksheet.write(n, m, _("Liquidation / M2"))
        m += 1
        worksheet.write(n, m, round(liquidation_amount / area, 3), three_decimal_format)
        n += 1
        m = 0
        worksheet.write(n, m, _("Weight Average"))
        m += 1
        average_weight = meat_kilos / output_unit if output_unit else 0
        worksheet.write(n, m, round(average_weight, 3), three_decimal_format)
        n += 1
        m = 0
        worksheet.write(n, m, _("Conversion"))
        m += 1
        conversion = feed_qty / meat_kilos if meat_kilos else 0
        worksheet.write(n, m, round(conversion, 3), three_decimal_format)
        n += 1
        m = 0
        worksheet.write(n, m, _("Difference"))
        m += 1
        worksheet.write(
            n, m, round(average_weight - conversion, 3), three_decimal_format
        )
        n += 1
        m = 0
        worksheet.write(n, m, _("Age Average"))
        m += 1
        average_age = (
            sum(objects.mapped("age_output")) / output_unit if output_unit else 0
        )
        worksheet.write(n, m, round(average_age, 2), two_decimal_format)
        n += 1
        m = 0
        worksheet.write(n, m, _("Growth Speed"))
        m += 1
        growth_speed = (
            meat_kilos / output_unit / average_age * 1000
            if output_unit and average_age
            else 0
        )
        worksheet.write(n, m, round(growth_speed, 2), two_decimal_format)
        n += 1
        m = 0
        worksheet.write(n, m, _("FEEP"))
        m += 1
        unit = (
            growth_speed * (100 - cancellation_percentage) / (10 * conversion)
            if cancellation_percentage and conversion
            else 0
        )
        worksheet.write(n, m, int(unit))
        n += 2
        m = 0
        worksheet.write(n, m, _("Totals"), table_header)
        for m in range(m + 1, 9):
            worksheet.write(n, m, "", table_header)
        n += 1
        m = 0
        worksheet.write(n, m, _("Breeding Nº"))
        m += 1
        worksheet.write(n, m, len(objects), int_format)
