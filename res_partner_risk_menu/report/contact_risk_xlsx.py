# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, fields, models
from odoo.exceptions import ValidationError


class ContactRiskXlsx(models.AbstractModel):
    _name = "report.contact_risk_xlsx"
    _inherit = "report.report_xlsx.abstract"
    _description = "Contact Risk Report"

    def generate_xlsx_report(self, workbook, data, objects):
        table_second_header = workbook.add_format(
            {
                "bold": True,
                "border": 1,
                "valign": "vcenter",
                "fg_color": "#afd095",
            }
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
        worksheet = workbook.add_worksheet("Contact Risk")
        n = 0
        worksheet.set_row(n, 45)
        worksheet.set_column(0, 0, 50)
        for i in range(1, 11):
            worksheet.set_column(1, i, 15)
        worksheet.write(n, 0, _("Description"), table_header)
        worksheet.write(n, 1, _("Date"), table_header)
        worksheet.write(n, 2, _("Number"), table_header)
        worksheet.write(n, 3, _("Invoice"), table_header)
        worksheet.write(n, 4, _("Order"), table_header)
        worksheet.write(n, 5, _("Amount"), table_header)
        worksheet.write(n, 6, _("Expiration Date"), table_header)
        worksheet.write(n, 7, _("Payment Date"), table_header)
        worksheet.write(n, 8, _("Discount Date"), table_header)
        worksheet.write(n, 9, _("Bank"), table_header)
        if len(objects) != 1:
            raise ValidationError(_("The report cant be taken from a single contact."))
        sales = objects.sale_order_ids
        sales += objects.child_ids.mapped("sale_order_ids")
        sales = sales.filtered(lambda c: c.state == "sale")
        n += 1
        for i in range(0, 10):
            worksheet.write(n, i, "", table_second_header)
        worksheet.write(n, 0, _("Delivery Pending Sales"), table_second_header)
        delivery_pending_sales = sales.filtered(
            lambda c: sum(c.order_line.mapped("qty_to_deliver")) > 0
        )
        worksheet.write(
            n,
            5,
            sum(delivery_pending_sales.mapped("amount_total"))
            if delivery_pending_sales
            else "",
            table_second_header,
        )
        for sale in delivery_pending_sales:
            n += 1
            m = 1
            worksheet.write(
                n,
                m,
                fields.Date.from_string(sale.date_order).strftime("%d-%m-%Y")
                if sale.date_order
                else "",
            )
            m += 1
            worksheet.write(n, m, sale.name if sale.name else "")
            m += 3
            worksheet.write(n, m, sale.amount_total, two_decimal_format)
        n += 1
        for i in range(0, 10):
            worksheet.write(n, i, "", table_second_header)
        worksheet.write(n, 0, _("Invoicing Pending Sales"), table_second_header)
        domain = objects.with_context(
            open_risk_field="risk_sale_order"
        ).open_risk_pivot_info()["domain"]
        s = self.env["sale.order.line"].search(domain)
        sales = []
        worksheet.write(
            n, 5, sum(s.mapped("risk_amount")) if s else "", table_second_header
        )
        for sale in s:
            if sale.order_id not in sales:
                risk_amount = sum(
                    s.filtered(lambda c: c.order_id == sale.order_id).mapped(
                        "risk_amount"
                    )
                )
                if risk_amount != 0:
                    sales.append(sale.order_id)
                    n += 1
                    m = 1
                    worksheet.write(
                        n,
                        m,
                        fields.Date.from_string(sale.date_order).strftime("%d-%m-%Y")
                        if sale.date_order
                        else "",
                    )
                    m += 1
                    worksheet.write(
                        n, m, sale.order_id.name if sale.order_id.name else ""
                    )
                    m += 3
                    worksheet.write(n, m, risk_amount, two_decimal_format)
        domain = objects.with_context(
            open_risk_field="risk_invoice_draft"
        ).open_risk_pivot_info()["domain"]
        invoices = self.env["account.move.line"].search(domain)
        inv = []
        n += 1
        for i in range(0, 10):
            worksheet.write(n, i, "", table_second_header)
        worksheet.write(n, 0, _("Draft Invoices"), table_second_header)
        worksheet.write(
            n,
            5,
            sum(invoices.mapped("amount_residual")) if invoices else "",
            table_second_header,
        )
        for invoice in invoices:
            if invoice.move_id not in inv:
                inv.append(invoice.move_id)
                n += 1
                m = 1
                worksheet.write(
                    n,
                    m,
                    fields.Date.from_string(invoice.invoice_date).strftime("%d-%m-%Y")
                    if invoice.invoice_date
                    else "",
                )
                m += 2
                worksheet.write(n, m, invoice.move_name if invoice.move_name else "")
                m += 2
                worksheet.write(n, m, invoice.amount_residual, two_decimal_format)
                m += 1
                worksheet.write(
                    n,
                    m,
                    fields.Date.from_string(invoice.move_id.invoice_date_due).strftime(
                        "%d-%m-%Y"
                    )
                    if invoice.move_id.invoice_date_due
                    else "",
                )
        n += 1
        for i in range(0, 10):
            worksheet.write(n, i, "", table_second_header)
        domain = objects.with_context(
            open_risk_field="risk_invoice_open"
        ).open_risk_pivot_info()["domain"]
        invoices = self.env["account.move.line"].search(domain)
        inv = []
        worksheet.write(n, 0, _("Invoices/Balance Open"), table_second_header)
        worksheet.write(
            n,
            5,
            sum(invoices.mapped("amount_residual")) if invoices else "",
            table_second_header,
        )
        for invoice in invoices:
            if invoice.move_id not in inv:
                inv.append(invoice.move_id)
                n += 1
                m = 1
                worksheet.write(
                    n,
                    m,
                    fields.Date.from_string(invoice.invoice_date).strftime("%d-%m-%Y")
                    if invoice.invoice_date
                    else "",
                )
                m += 2
                worksheet.write(n, m, invoice.move_name if invoice.move_name else "")
                m += 2
                worksheet.write(n, m, invoice.amount_residual, two_decimal_format)
                m += 1
                worksheet.write(
                    n,
                    m,
                    fields.Date.from_string(invoice.move_id.invoice_date_due).strftime(
                        "%d-%m-%Y"
                    )
                    if invoice.move_id.invoice_date_due
                    else "",
                )
        n += 1
        for i in range(0, 10):
            worksheet.write(n, i, "", table_second_header)
        domain = objects.with_context(
            open_risk_field="risk_invoice_unpaid"
        ).open_risk_pivot_info()["domain"]
        invoices = self.env["account.move.line"].search(domain)
        inv = []
        worksheet.write(n, 0, _("Invoices/Balance Open"), table_second_header)
        worksheet.write(
            n,
            5,
            sum(invoices.mapped("amount_residual")) if invoices else "",
            table_second_header,
        )
        for invoice in invoices:
            if invoice.move_id not in inv:
                inv.append(invoice.move_id)
                n += 1
                m = 1
                worksheet.write(
                    n,
                    m,
                    fields.Date.from_string(invoice.invoice_date).strftime("%d-%m-%Y")
                    if invoice.invoice_date
                    else "",
                )
                m += 2
                worksheet.write(n, m, invoice.move_name if invoice.move_name else "")
                m += 2
                worksheet.write(n, m, invoice.amount_residual, two_decimal_format)
                m += 1
                worksheet.write(
                    n,
                    m,
                    fields.Date.from_string(invoice.move_id.invoice_date_due).strftime(
                        "%d-%m-%Y"
                    )
                    if invoice.move_id.invoice_date_due
                    else "",
                )
        n += 1
        for i in range(0, 10):
            worksheet.write(n, i, "", table_second_header)
        domain = objects.with_context(
            open_risk_field="risk_account_amount"
        ).open_risk_pivot_info()["domain"]
        invoices = self.env["account.move.line"].search(domain)
        inv = []
        worksheet.write(n, 0, _("Other Open Account Balance"), table_second_header)
        worksheet.write(
            n,
            5,
            sum(invoices.mapped("amount_residual")) if invoices else "",
            table_second_header,
        )
        for invoice in invoices:
            if invoice.move_id not in inv:
                inv.append(invoice.move_id)
                n += 1
                m = 1
                worksheet.write(
                    n,
                    m,
                    fields.Date.from_string(invoice.invoice_date).strftime("%d-%m-%Y")
                    if invoice.invoice_date
                    else "",
                )
                m += 2
                worksheet.write(n, m, invoice.move_name if invoice.move_name else "")
                m += 2
                worksheet.write(n, m, invoice.amount_residual, two_decimal_format)
                m += 1
                worksheet.write(
                    n,
                    m,
                    fields.Date.from_string(invoice.move_id.invoice_date_due).strftime(
                        "%d-%m-%Y"
                    )
                    if invoice.move_id.invoice_date_due
                    else "",
                )
        n += 1
        for i in range(0, 10):
            worksheet.write(n, i, "", table_second_header)
        domain = objects.with_context(
            open_risk_field="risk_account_amount_unpaid"
        ).open_risk_pivot_info()["domain"]
        invoices = self.env["account.move.line"].search(domain)
        inv = []
        worksheet.write(n, 0, _("Other Unpaid Account Balance"), table_second_header)
        worksheet.write(
            n,
            5,
            sum(invoices.mapped("amount_residual")) if invoices else "",
            table_second_header,
        )
        for invoice in invoices:
            if invoice.move_id not in inv:
                inv.append(invoice.move_id)
                n += 1
                m = 1
                worksheet.write(
                    n,
                    m,
                    fields.Date.from_string(invoice.invoice_date).strftime("%d-%m-%Y")
                    if invoice.invoice_date
                    else "",
                )
                m += 2
                worksheet.write(n, m, invoice.move_name if invoice.move_name else "")
                m += 2
                worksheet.write(n, m, invoice.amount_residual, two_decimal_format)
                m += 1
                worksheet.write(
                    n,
                    m,
                    fields.Date.from_string(invoice.move_id.invoice_date_due).strftime(
                        "%d-%m-%Y"
                    )
                    if invoice.move_id.invoice_date_due
                    else "",
                )
        n += 1
        for i in range(0, 10):
            worksheet.write(n, i, "", table_second_header)
        worksheet.write(n, 0, _("Risk Sum"), table_second_header)
        worksheet.write(n, 5, objects.risk_sum, table_second_header)
        n += 1
        for i in range(0, 10):
            worksheet.write(n, i, "", table_second_header)
        worksheet.write(n, 0, _("Credit Policy"), table_second_header)
        worksheet.write(n, 5, objects.credit_policy_amount, table_second_header)
        n += 1
        for i in range(0, 10):
            worksheet.write(n, i, "", table_second_header)
        worksheet.write(n, 0, _("Total Risk"), table_second_header)
        worksheet.write(n, 5, objects.risk_total_amount, table_second_header)
