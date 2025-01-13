# Copyright 2024 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import base64
import logging
import os
import tempfile
from collections import defaultdict

from odoo import api, fields, models, tools

_logger = logging.getLogger(__name__)

try:
    from statistics import mean

    STATS_PATH = tools.find_in_path("statistics")
except (ImportError, IOError) as err:
    _logger.debug(err)

try:
    import xlsxwriter

except ImportError:
    _logger.debug("Can not import xlsxwriter`.")


class AccountInvoiceXLSXExport(models.TransientModel):
    _name = "account.invoice.breakdown.export"

    invoice_ids = fields.Many2many(
        comodel_name="account.move",
    )
    invoice_count = fields.Integer(
        compute="_compute_invoice_count",
    )

    @api.depends("invoice_ids")
    def _compute_invoice_count(self):
        for record in self:
            record.invoice_count = len(record.invoice_ids)

    @api.model
    def default_get(self, fields):
        rec = super().default_get(fields)
        active_model = self.env.context.get("active_model")
        if active_model == "account.move":
            invoices = (
                self.env[active_model]
                .browse(self.env.context.get("active_ids"))
                .exists()
                .filtered(lambda inv: inv.is_invoice() and inv.state == "posted")
            )
            rec.update(invoice_ids=[(6, 0, invoices.ids)])
        return rec

    def export_invoices(self):
        self.ensure_one()
        filename = "Listado_Facturas.xlsx"
        filepath = tempfile.gettempdir() + "/" + filename

        workbook = xlsxwriter.Workbook(filepath, {"default_date_format": "dd/mm/yyyy"})
        currency_id = self.env["res.company"]._default_currency_id()

        # Styles
        # title = workbook.add_format(
        #     {
        #         "bold": True,
        #         "align": "center",
        #         "valign": "vcenter",
        #     }
        # )
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
        table_detail_left = workbook.add_format(
            {
                "border": 1,
                "align": "left",
                "valign": "vcenter",
            }
        )
        table_detail_right_num = workbook.add_format(
            {
                "border": 1,
                "align": "right",
                "valign": "vcenter",
                "num_format": "#,##0." + "0" * currency_id.decimal_places,
            }
        )
        table_detail_date = workbook.add_format(
            {
                "border": 1,
                "align": "right",
                "valign": "vcenter",
                "num_format": "dd/mm/yyyy",  # diamacon format
            }
        )

        for move_type in self.invoice_ids.get_invoice_types(include_receipts=False):
            invoices = self.invoice_ids.filtered(lambda m: m.move_type == move_type)
            if invoices:
                all_taxes = (
                    self.invoice_ids.mapped("line_ids")
                    .mapped("tax_line_id")
                    .flatten_taxes_hierarchy()
                    .mapped("tax_group_id")
                    .sorted()
                )

                worksheet = workbook.add_worksheet(move_type)
                worksheet.write(0, 0, "Invoice Number", table_header)
                worksheet.write(0, 1, "Invoice Date", table_header)
                worksheet.write(0, 2, "Partner", table_header)
                worksheet.write(0, 3, "Concept", table_header)
                worksheet.set_column(0, 3, 32)
                worksheet.write(0, 4, "Amount Untaxed", table_header)
                worksheet.write(0, 5, "Amount Taxed", table_header)
                worksheet.set_column(4, 5, 15)

                start_tax_col_num = tax_col_num = 6
                for tax in all_taxes:
                    worksheet.write(0, tax_col_num, tax.display_name, table_header)
                    worksheet.write(
                        0, tax_col_num + 1, "%s base" % (tax.display_name), table_header
                    )
                    worksheet.write(
                        0,
                        tax_col_num + 2,
                        "%s amount" % (tax.display_name),
                        table_header,
                    )
                    worksheet.set_column(tax_col_num, tax_col_num + 2, 15)
                    tax_col_num += 3

                row_num = 1
                for invoice in invoices:
                    # diamacon does not accept special characters
                    invoice_num = "".join(
                        letter for letter in invoice.name if letter.isalnum()
                    )
                    # diamacon only accepts up to 8 characters
                    worksheet.write(row_num, 0, invoice_num[-8:], table_detail_left)
                    worksheet.write_datetime(
                        row_num,
                        1,
                        invoice.invoice_date,
                        table_detail_date,
                    )
                    worksheet.write(
                        row_num,
                        2,
                        invoice.invoice_partner_display_name,
                        table_detail_left,
                    )
                    # worksheet.write(row_num, 3, "Concept", table_detail_left)
                    worksheet.write(
                        row_num,
                        4,
                        invoice.amount_untaxed_signed,
                        table_detail_right_num,
                    )
                    worksheet.write(
                        row_num, 5, invoice.amount_total_signed, table_detail_right_num
                    )

                    tax_group_mapping = defaultdict(
                        lambda: {
                            "base_lines": set(),
                            "tax_percent": [],
                            "base_amount": 0.0,
                            "tax_amount": 0.0,
                        }
                    )

                    balance_multiplicator = -1 if invoice.is_inbound() else 1
                    tax_lines = invoice.line_ids.filtered("tax_line_id")
                    base_lines = invoice.line_ids.filtered("tax_ids")

                    for base_line in base_lines:
                        base_amount = balance_multiplicator * (
                            base_line.amount_currency
                            if base_line.currency_id
                            else base_line.balance
                        )

                        for tax in base_line.tax_ids.flatten_taxes_hierarchy():

                            if base_line.tax_line_id.tax_group_id == tax.tax_group_id:
                                continue

                            tax_group_vals = tax_group_mapping[tax.tax_group_id]
                            tax_group_vals["tax_percent"].append(tax.amount)
                            if base_line not in tax_group_vals["base_lines"]:
                                tax_group_vals["base_amount"] += base_amount
                                tax_group_vals["base_lines"].add(base_line)

                    # Compute tax amounts.
                    for tax_line in tax_lines:
                        tax_amount = balance_multiplicator * (
                            tax_line.amount_currency
                            if tax_line.currency_id
                            else tax_line.balance
                        )
                        tax_group_vals = tax_group_mapping[
                            tax_line.tax_line_id.tax_group_id
                        ]
                        tax_group_vals["tax_amount"] += tax_amount

                    tax_col_num = start_tax_col_num
                    for tax_group in all_taxes:
                        tax_group_vals = tax_group_mapping[tax_group]
                        if not tax_group_vals:
                            pass
                        tax_percent = (
                            mean(tax_group_vals["tax_percent"])
                            if tax_group_vals["tax_percent"]
                            else 0.0
                        )
                        worksheet.write(
                            row_num,
                            tax_col_num,
                            tax_percent,
                            table_detail_right_num,
                        )
                        worksheet.write(
                            row_num,
                            tax_col_num + 1,
                            tax_group_vals["base_amount"],
                            table_detail_right_num,
                        )
                        worksheet.write(
                            row_num,
                            tax_col_num + 2,
                            tax_group_vals["tax_amount"],
                            table_detail_right_num,
                        )
                        tax_col_num += 3

                    row_num += 1

        workbook.close()

        fp = open(filepath, "rb")
        file_data = fp.read()
        excel_file = base64.encodestring(file_data)
        fp.close()

        # Crear fichero temporal
        datafile_fd, datafile_path = tempfile.mkstemp(suffix=filename)
        os.close(datafile_fd)

        # CREAR ADJUNTO
        with open(datafile_path, "r"):  # as datafile:
            res = {
                "name": filename,
                "datas": excel_file,
                "res_model": self._name,
                "res_id": self.id,
                "type": "binary",
            }
        try:  # Borrar archivo temporal
            os.unlink(datafile_path)
        except Exception:
            pass
        attach = self.env["ir.attachment"].create(res)
        # self.env.cr.commit()
        url = "/web/content/%s?download=true" % attach.id
        return {
            "type": "ir.actions.act_url",
            "url": url,
            "target": "new",
        }
