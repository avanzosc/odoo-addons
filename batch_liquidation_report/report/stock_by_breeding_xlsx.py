# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from datetime import datetime

from odoo import _, fields, models


class StockByBreedingXlsx(models.AbstractModel):
    _name = "report.stock_by_breeding_xlsx"
    _inherit = "report.report_xlsx.abstract"
    _description = "Stock By Breeding Report"

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
        table_header.set_text_wrap()
        int_format.set_text_wrap()
        two_decimal_format.set_text_wrap()
        table_detail_right_num = workbook.add_format(
            {
                "border": 1,
                "align": "right",
                "valign": "vcenter",
            }
        )
        table_detail_right_num.set_num_format("#,##0.00")
        worksheet = workbook.add_worksheet("Live Breedings Stock")
        n = 0
        worksheet.set_row(n, 45)
        for i in range(0, 14):
            worksheet.set_column(0, i, 14)
        worksheet.write(n, 0, _("Breeding"), table_header)
        worksheet.write(n, 1, _("Date"), table_header)
        worksheet.write(n, 2, _("Cleaning Date"), table_header)
        worksheet.write(n, 3, _("Description"), table_header)
        worksheet.write(n, 4, _("Entry Chick (Units)"), table_header)
        worksheet.write(n, 5, _("Output Chicken (Meat Units)"), table_header)
        worksheet.write(n, 6, _("Stock (E - O Units)"), table_header)
        worksheet.write(n, 7, _("Chicken Amount"), table_header)
        worksheet.write(n, 8, _("Feed Amount"), table_header)
        worksheet.write(n, 9, _("Medicine Amount"), table_header)
        worksheet.write(n, 10, _("Costs"), table_header)
        worksheet.write(n, 11, _("Output Chicken Qty"), table_header)
        worksheet.write(n, 12, _("Amount"), table_header)
        worksheet.write(n, 13, _("Difference"), table_header)
        chick_type = self.env.ref("stock_picking_batch_liquidation.move_type1")
        meat_type = self.env.ref("stock_picking_batch_liquidation.move_type3")
        medicine_type = self.env.ref("stock_picking_batch_liquidation.move_type4")
        feed_type = self.env.ref("stock_picking_batch_liquidation.move_type5")
        meat_cost = 0
        date = fields.Date.today()
        if "date" in data:
            date = data["date"]
            date = datetime.strptime(date, "%Y-%m-%d").date()
        if "meat_cost" in data:
            meat_cost = data["meat_cost"]
        batches = []
        if "objects" in data:
            batches = self.env["stock.picking.batch"].browse(data.get("objects"))
        for line in batches:
            n += 1
            worksheet.write(n, 0, line.name if line.name else "")
            if line.entry_date:
                worksheet.write(
                    n,
                    1,
                    fields.Date.from_string(line.entry_date).strftime("%d-%m-%Y")
                    if line.entry_date
                    else "",
                )
            if line.cleaned_date:
                worksheet.write(
                    n,
                    2,
                    fields.Date.from_string(line.cleaned_date).strftime("%d-%m-%Y")
                    if line.entry_date
                    else "",
                )
            worksheet.write(n, 3, line.warehouse_id.name if line.warehouse_id else "")
            chick_lines = line.move_line_ids.filtered(
                lambda c: c.move_type_id == chick_type
                and c.picking_id
                and (c.date.date() <= date)
            )
            entry_chick_lines = chick_lines.filtered(
                lambda c: c.location_dest_id == line.location_id
            )
            dev_chick_lines = chick_lines.filtered(
                lambda c: c.location_id == line.location_id
            )
            chick_units = sum(entry_chick_lines.mapped("download_unit")) - sum(
                dev_chick_lines.mapped("download_unit")
            )
            worksheet.write(n, 4, chick_units)
            meat_lines = line.move_line_ids.filtered(
                lambda c: c.move_type_id == meat_type
                and c.picking_id
                and (c.date.date() <= date)
            )
            output_meat_lines = meat_lines.filtered(
                lambda c: c.location_id == line.location_id
            )
            dev_meat_lines = meat_lines.filtered(
                lambda c: c.location_dest_id == line.location_id
            )
            meat_units = sum(output_meat_lines.mapped("download_unit")) - sum(
                dev_meat_lines.mapped("download_unit")
            )
            worksheet.write(n, 5, meat_units)
            worksheet.write(n, 6, chick_units - meat_units)
            chick_amount = sum(entry_chick_lines.mapped("amount")) - sum(
                dev_chick_lines.mapped("amount")
            )
            worksheet.write(n, 7, chick_amount, two_decimal_format)
            stock_feed = self.env["stock.quant"].search(
                [
                    ("location_id", "=", line.location_id.id),
                    ("move_type_id", "=", feed_type.id),
                ]
            )
            lots = stock_feed.mapped("lot_id")
            all_feed_lines = line.move_line_ids.filtered(
                lambda c: c.move_type_id == feed_type and c.picking_id
            )
            all_breeding_lots = all_feed_lines.mapped("lot_id")
            dif_lots = lots - all_breeding_lots
            quant_amount = 0
            for lot in dif_lots:
                quant_amount += sum(
                    stock_feed.filtered(lambda c: c.lot_id == lot).mapped("value")
                )
            feed_lines = line.move_line_ids.filtered(
                lambda c: c.move_type_id == feed_type
                and c.picking_id
                and (c.date.date() <= date)
            )
            entry_feed_lines = feed_lines.filtered(
                lambda c: c.location_dest_id == line.location_id
            )
            dev_feed_lines = feed_lines.filtered(
                lambda c: c.location_id == line.location_id
            )
            feed_amount = (
                sum(entry_feed_lines.mapped("amount"))
                - sum(dev_feed_lines.mapped("amount"))
                + quant_amount
            )
            worksheet.write(n, 8, feed_amount, two_decimal_format)
            medicine_lines = line.move_line_ids.filtered(
                lambda c: c.move_type_id == medicine_type
                and (c.picking_id)
                and c.date.date() <= date
            )
            entry_medicine_lines = medicine_lines.filtered(
                lambda c: c.location_dest_id == line.location_id
            )
            dev_medicine_lines = medicine_lines.filtered(
                lambda c: c.location_id == line.location_id
            )
            medicine_amount = sum(entry_medicine_lines.mapped("amount")) - sum(
                dev_medicine_lines.mapped("amount")
            )
            worksheet.write(n, 9, medicine_amount, two_decimal_format)
            cost_amount = chick_amount + feed_amount + medicine_amount
            worksheet.write(n, 10, cost_amount, two_decimal_format)
            meat_qty_done = sum(output_meat_lines.mapped("qty_done")) - sum(
                dev_meat_lines.mapped("qty_done")
            )
            worksheet.write(n, 11, meat_qty_done, two_decimal_format)
            meat_amount = meat_qty_done * meat_cost
            worksheet.write(n, 12, meat_amount, two_decimal_format)
            worksheet.write(n, 13, cost_amount - meat_amount, two_decimal_format)
