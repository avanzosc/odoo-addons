# Copyright 2025 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, fields, models
from odoo.exceptions import ValidationError


class ContactRiskXlsxOpt(models.AbstractModel):
    _name = "report.contact_risk_xlsx_opt"
    _inherit = "report.report_xlsx.abstract"
    _description = "Contact Risk Report Optimized"

    def _prepare_formats(self, workbook):
        table_second_header = workbook.add_format(
            {"bold": True, "border": 1, "valign": "vcenter", "fg_color": "#afd095"}
        )
        table_header = workbook.add_format(
            {
                "bold": True,
                "border": 1,
                "align": "center",
                "valign": "vcenter",
                "fg_color": "#D7E4BC",
            }
        )
        two_decimal_format = workbook.add_format({"num_format": "#,##0.00;(#,##0.00)"})
        table_header.set_text_wrap()
        two_decimal_format.set_text_wrap()
        return {
            "section": table_second_header,
            "header": table_header,
            "decimal": two_decimal_format,
        }

    def _prepare_worksheet(self, workbook):
        worksheet = workbook.add_worksheet("Contact Risk")
        worksheet.set_row(0, 45)
        worksheet.set_column(0, 0, 50)
        worksheet.set_column(1, 10, 15)
        return worksheet

    @staticmethod
    def _format_date(date_str):
        return (
            fields.Date.from_string(date_str).strftime("%d-%m-%Y") if date_str else ""
        )

    @staticmethod
    def _write_blank_row(worksheet, row, row_format):
        for col in range(10):
            worksheet.write(row, col, "", row_format)

    def _write_headers(self, worksheet, header_format):
        headers = [
            _("Description"),
            _("Date"),
            _("Number"),
            _("Invoice"),
            _("Order"),
            _("Amount"),
            _("Expiration Date"),
            _("Payment Date"),
            _("Discount Date"),
            _("Bank"),
        ]
        for col, text in enumerate(headers):
            worksheet.write(0, col, text, header_format)

    def _write_total_row(
        self, worksheet, row, title, amount, section_format, blank_when_zero=True
    ):
        row += 1
        self._write_blank_row(worksheet, row, section_format)
        worksheet.write(row, 0, title, section_format)
        value = "" if blank_when_zero and not amount else amount
        worksheet.write(row, 5, value, section_format)
        return row

    def _write_delivery_pending_sales(self, worksheet, row, partner, formats):
        row = self._write_total_row(
            worksheet, row, _("Delivery Pending Sales"), 0.0, formats["section"]
        )
        sales = (
            partner.sale_order_ids | partner.child_ids.mapped("sale_order_ids")
        ).filtered(lambda sale: sale.state == "sale")
        delivery_pending_sales = sales.filtered(
            lambda sale: sum(sale.order_line.mapped("qty_to_deliver")) > 0
        )
        total_pending = sum(delivery_pending_sales.mapped("amount_total"))
        worksheet.write(
            row,
            5,
            total_pending if total_pending else "",
            formats["section"],
        )
        for sale in delivery_pending_sales:
            row += 1
            worksheet.write(row, 1, self._format_date(sale.date_order))
            worksheet.write(row, 2, sale.name or "")
            worksheet.write(row, 5, sale.amount_total, formats["decimal"])
        return row

    def _write_invoicing_pending_sales(self, worksheet, row, partner, formats):
        row = self._write_total_row(
            worksheet, row, _("Invoicing Pending Sales"), 0.0, formats["section"]
        )
        domain = partner.with_context(
            open_risk_field="risk_sale_order"
        ).open_risk_pivot_info()["domain"]
        sale_lines = self.env["sale.order.line"].search(domain)
        order_amounts = {}
        for line in sale_lines:
            order_amounts.setdefault(line.order_id, 0.0)
            order_amounts[line.order_id] += line.risk_amount
        total = sum(order_amounts.values())
        worksheet.write(row, 5, total if total else "", formats["section"])
        for order, amount in order_amounts.items():
            if not amount:
                continue
            row += 1
            worksheet.write(row, 1, self._format_date(order.date_order))
            worksheet.write(row, 2, order.name or "")
            worksheet.write(row, 5, amount, formats["decimal"])
        return row

    def _write_invoice_section(self, worksheet, row, title, records, formats):
        row = self._write_total_row(
            worksheet,
            row,
            title,
            sum(records.mapped("amount_residual")) if records else 0.0,
            formats["section"],
        )
        seen_move_ids = set()
        for record in records:
            move_id = record.move_id.id
            if not move_id or move_id in seen_move_ids:
                continue
            seen_move_ids.add(move_id)
            row += 1
            worksheet.write(row, 1, self._format_date(record.invoice_date))
            worksheet.write(row, 3, record.move_name or "")
            worksheet.write(row, 5, record.amount_residual, formats["decimal"])
            worksheet.write(row, 6, self._format_date(record.move_id.invoice_date_due))
        return row

    def _write_risk_sections(self, worksheet, row, partner, formats):
        risk_fields = [
            ("risk_invoice_draft", _("Draft Invoices")),
            ("risk_invoice_open", _("Invoices/Balance Open")),
            ("risk_invoice_unpaid", _("Invoices/Balance Open")),
            ("risk_account_amount", _("Other Open Account Balance")),
            ("risk_account_amount_unpaid", _("Other Unpaid Account Balance")),
        ]
        for risk_field, label in risk_fields:
            domain = partner.with_context(
                open_risk_field=risk_field
            ).open_risk_pivot_info()["domain"]
            invoice_lines = self.env["account.move.line"].search(domain)
            row = self._write_invoice_section(
                worksheet, row, label, invoice_lines, formats
            )
        return row

    def _write_risk_totals(self, worksheet, row, partner, formats):
        for label, amount in [
            (_("Risk Sum"), partner.risk_sum),
            (_("Credit Policy"), partner.credit_policy_amount),
            (_("Total Risk"), partner.risk_total_amount),
        ]:
            row = self._write_total_row(
                worksheet,
                row,
                label,
                amount,
                formats["section"],
                blank_when_zero=False,
            )
        return row

    def generate_xlsx_report(self, workbook, data, objects):
        if len(objects) != 1:
            raise ValidationError(_("The report cant be taken from a single contact."))

        partner = objects
        formats = self._prepare_formats(workbook)
        worksheet = self._prepare_worksheet(workbook)
        self._write_headers(worksheet, formats["header"])

        row = 0
        row = self._write_delivery_pending_sales(worksheet, row, partner, formats)
        row = self._write_invoicing_pending_sales(worksheet, row, partner, formats)
        row = self._write_risk_sections(worksheet, row, partner, formats)
        self._write_risk_totals(worksheet, row, partner, formats)
