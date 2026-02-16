# Copyright 2025 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, fields, models
from odoo.exceptions import ValidationError


class ContactRiskXlsxOpt(models.AbstractModel):
    _name = "report.contact_risk_xlsx_opt"
    _inherit = "report.report_xlsx.abstract"
    _description = "Contact Risk Report Optimized"

    def generate_xlsx_report(self, workbook, data, objects):
        def _write_blank_row(n):
            for i in range(10):
                worksheet.write(n, i, "", table_second_header)

        def _format_date(date_str):
            return (
                fields.Date.from_string(date_str).strftime("%d-%m-%Y")
                if date_str
                else ""
            )

        def _write_section(title, records, amount_field, key_field="move_id"):
            nonlocal n
            n += 1
            _write_blank_row(n)
            worksheet.write(n, 0, title, table_second_header)
            total = sum(getattr(r, amount_field, 0.0) for r in records)
            worksheet.write(n, 5, total if total else "", table_second_header)

            seen = set()
            for rec in records:
                key = getattr(rec, key_field, None)
                if not key or key in seen:
                    continue
                seen.add(key)
                n += 1
                m = 1
                worksheet.write(n, m, _format_date(getattr(rec, "invoice_date", False)))
                m += 2
                worksheet.write(n, m, getattr(rec, "move_name", "") or "")
                m += 2
                worksheet.write(
                    n, m, getattr(rec, amount_field, 0.0), two_decimal_format
                )
                m += 1
                due_date = getattr(
                    getattr(rec, "move_id", None), "invoice_date_due", False
                )
                worksheet.write(n, m, _format_date(due_date))

        # --- FORMATS ---
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
        int_format = workbook.add_format({"num_format": "#,##0;(#,##0)"})
        two_decimal_format = workbook.add_format({"num_format": "#,##0.00;(#,##0.00)"})
        for f in (table_header, int_format, two_decimal_format):
            f.set_text_wrap()
        table_detail_right_num = workbook.add_format(
            {"border": 1, "align": "right", "valign": "vcenter"}
        )
        table_detail_right_num.set_num_format("#,##0.00")

        # --- SHEET ---
        worksheet = workbook.add_worksheet("Contact Risk")
        worksheet.set_row(0, 45)
        worksheet.set_column(0, 0, 50)
        worksheet.set_column(1, 10, 15)

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
            worksheet.write(0, col, text, table_header)

        if len(objects) != 1:
            raise ValidationError(_("The report cant be taken from a single contact."))

        n = 0
        # --- SALES (pending delivery) ---
        n += 1
        _write_blank_row(n)
        worksheet.write(n, 0, _("Delivery Pending Sales"), table_second_header)
        sales = (
            objects.sale_order_ids | objects.child_ids.mapped("sale_order_ids")
        ).filtered(lambda s: s.state == "sale")
        delivery_pending_sales = sales.filtered(
            lambda c: sum(c.order_line.mapped("qty_to_deliver")) > 0
        )
        total_pending = sum(delivery_pending_sales.mapped("amount_total"))
        worksheet.write(
            n, 5, total_pending if total_pending else "", table_second_header
        )
        for sale in delivery_pending_sales:
            n += 1
            worksheet.write(n, 1, _format_date(sale.date_order))
            worksheet.write(n, 2, sale.name or "")
            worksheet.write(n, 5, sale.amount_total, two_decimal_format)

        # --- SALES (pending invoicing) ---
        n += 1
        _write_blank_row(n)
        worksheet.write(n, 0, _("Invoicing Pending Sales"), table_second_header)
        domain = objects.with_context(
            open_risk_field="risk_sale_order"
        ).open_risk_pivot_info()["domain"]
        sale_lines = self.env["sale.order.line"].search(domain)
        if sale_lines:
            order_amounts = {}
            for line in sale_lines:
                order_amounts.setdefault(line.order_id, 0.0)
                order_amounts[line.order_id] += line.risk_amount
            total = sum(order_amounts.values())
            worksheet.write(n, 5, total, table_second_header)
            for order, amount in order_amounts.items():
                if not amount:
                    continue
                n += 1
                worksheet.write(n, 1, _format_date(order.date_order))
                worksheet.write(n, 2, order.name or "")
                worksheet.write(n, 5, amount, two_decimal_format)

        # --- INVOICES ---
        risk_fields = [
            ("risk_invoice_draft", _("Draft Invoices")),
            ("risk_invoice_open", _("Invoices/Balance Open")),
            ("risk_invoice_unpaid", _("Invoices/Balance Open")),
            ("risk_account_amount", _("Other Open Account Balance")),
            ("risk_account_amount_unpaid", _("Other Unpaid Account Balance")),
        ]

        for field, label in risk_fields:
            domain = objects.with_context(open_risk_field=field).open_risk_pivot_info()[
                "domain"
            ]
            invoices = self.env["account.move.line"].search(domain)
            _write_section(label, invoices, "amount_residual")

        # --- RISK TOTALS ---
        for label, value in [
            (_("Risk Sum"), objects.risk_sum),
            (_("Credit Policy"), objects.credit_policy_amount),
            (_("Total Risk"), objects.risk_total_amount),
        ]:
            n += 1
            _write_blank_row(n)
            worksheet.write(n, 0, label, table_second_header)
            worksheet.write(n, 5, value, table_second_header)
