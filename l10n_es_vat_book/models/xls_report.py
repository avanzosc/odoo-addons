# -*- coding: utf-8 -*-
# Copyright 2014 Anubía, soluciones en la nube,SL (http://www.anubia.es)
# Copyright Juan Formoso <jfv@anubia.es>
# Copyright Alejandro Santana <alejandrosantana@anubia.es>
# Copyright Pedro M. Baeza <pedro.baeza@tecnativa.com>
# Copyright 2017 valentin vinagre <valentin.vinagre@qubiq.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

try:
    from openerp.addons.report_xlsx.report.report_xlsx import ReportXlsx
    from xlsxwriter.utility import xl_rowcol_to_cell
except ImportError:
    ReportXlsx = object
from openerp.report import report_sxw
import numpy as np
from datetime import datetime
from openerp import _
from array import array

class IvaXlsx(ReportXlsx):
    def __init__(self, name, table, rml=False, parser=False, header=True,
                 store=False):
        super(ReportXlsx, self).__init__(
            name, table, rml, parser, header, store)
        self.sheet = None
        self.row_pos = None
        self.format_title = None
        self.format_border_top = None
        self.money_format = None
        self.format_bold = None
        self.format_total = None
        self.format_total_title = None
        self.existTable = True

    def _define_formats(self, workbook):
        """ Add cell formats to current workbook.
        Available formats:
         * format_title
         * format_header
        """
        self.format_title = workbook.add_format({
            'bold': True,
            'align': 'center',
            'font_size': 14,
            'bg_color': '#FFF58C',
            'border': True
        })
        self.format_resumen = workbook.add_format({
            'border': True
        })
        self.format_header = workbook.add_format({
            'bold': True,
            'align': 'center',
            'bg_color': '#FFFFCC',
            'border': True
        })
        self.format_field = workbook.add_format({
            'bold': True,
            'bg_color': '#FFFFCC',
            'border': True
        })

        self.format_bold = workbook.add_format({
            'bold': True,
            'border': True,
            'num_format': '0.00'
        })

        self.format_total = workbook.add_format({
            'bold': True,
            'border': True,
            'num_format': '#,##0.00',
            # 'bg_color': '#3BEFE6'
        })

        self.format_total_title = workbook.add_format({
            'bold': True,

        })

        self.num_format = workbook.add_format({'num_format': '#,##0.00'})

        self.date_format = workbook.add_format({'num_format': 'dd-mm-yyyy'})
        self.porcentaje_format = workbook.add_format({'num_format': '0.00%'})

    def _write_report_title(self, title):
        initial_row = self.row_pos
        for sheet in self.sheets:
            self.row_pos = initial_row + 1
            if sheet.index == 1:
                sheet.merge_range(
                    self.row_pos, 0, self.row_pos, 9, sheet.name, self.format_title
                )
            else:
                sheet.merge_range(
                self.row_pos, 0, self.row_pos, 8, sheet.name, self.format_title
                )
            self.row_pos += 2

    def _write_report_attributes(self, objects):
        initial_row = self.row_pos
        for sheet in self.sheets:
            if sheet.index == 1:
                self.row_pos= initial_row + 1
                sheet.write_string(self.row_pos, 2, _('Company'), self.format_field)
                sheet.write_string(self.row_pos, 3, objects.company_id.name )
                sheet.merge_range(self.row_pos, 4, self.row_pos, 5, _('VAT'), self.format_field)
                sheet.write_string(self.row_pos, 6, objects.company_vat)
                self.row_pos += 1
                sheet.write_string(self.row_pos, 2, _('Fiscal Year'), self.format_field)
                sheet.write_string(self.row_pos, 3, objects.fiscalyear_id.name)
                sheet.merge_range(self.row_pos, 4, self.row_pos, 5,_('Contact phone'), self.format_field)
                sheet.write_string(self.row_pos, 6, objects.contact_phone)
                self.row_pos += 1
                sheet.write_string(self.row_pos, 2, _('Periods'), self.format_field)
                sheet.write_string(self.row_pos, 3, dict(objects.fields_get(allfields=['period_type'])['period_type']['selection'])[objects.period_type])
                sheet.merge_range(self.row_pos, 4, self.row_pos, 5,_('Surnames and name contact'), self.format_field)
                sheet.write_string(self.row_pos, 6, objects.contact_name)
                self.row_pos += 2
            else:
                self.row_pos= initial_row + 1
                sheet.write_string(self.row_pos, 1, _('Company'), self.format_field)
                sheet.write_string(self.row_pos, 2, objects.company_id.name )
                sheet.merge_range(self.row_pos, 3, self.row_pos, 4, _('VAT'), self.format_field)
                sheet.write_string(self.row_pos, 5, objects.company_vat)
                self.row_pos += 1
                sheet.write_string(self.row_pos, 1, _('Fiscal Year'), self.format_field)
                sheet.write_string(self.row_pos, 2, objects.fiscalyear_id.name)
                sheet.merge_range(self.row_pos, 3, self.row_pos, 4,_('Contact phone'), self.format_field)
                sheet.write_string(self.row_pos, 5, objects.contact_phone)
                self.row_pos += 1
                sheet.write_string(self.row_pos, 1, _('Periods'), self.format_field)
                sheet.write_string(self.row_pos, 2, dict(objects.fields_get(allfields=['period_type'])['period_type']['selection'])[objects.period_type])
                sheet.merge_range(self.row_pos, 3, self.row_pos, 4,_('Surnames and name contact'), self.format_field)
                sheet.write_string(self.row_pos, 5, objects.contact_name)
                self.row_pos += 2

    def _set_headers(self):
        initial_row = self.row_pos
        for sheet in self.sheets:
            if sheet.index != 1:
                self.row_pos= initial_row + 1
                sheet.set_column(0, 0, 13)
                sheet.write_string(self.row_pos, 0, _('Invoice date'), self.format_header)
                sheet.set_column(1, 1, 18)
                sheet.write_string(self.row_pos, 1, _('Invoice number'), self.format_header)
                sheet.set_column(2, 2, 55)
                sheet.write_string(self.row_pos, 2, _('Company'), self.format_header)
                sheet.set_column(3, 3, 15)
                sheet.write_string(self.row_pos, 3, _('VAT'), self.format_header)
                sheet.set_column(4, 4, 30)
                sheet.write_string(self.row_pos, 4, _('Code'), self.format_header)
                sheet.set_column(5, 5, 15)
                sheet.write_string(self.row_pos, 5, _('Base'), self.format_header)
                sheet.set_column(6, 6, 15)
                sheet.write_string(self.row_pos, 6, _('Type'), self.format_header)
                sheet.set_column(7, 7, 15)
                sheet.write_string(self.row_pos, 7, _('Cuote'), self.format_header)
                sheet.set_column(8, 8, 15)
                sheet.write_string(self.row_pos, 8, _('Total'), self.format_header)
            else:
                self.row_pos = initial_row + 1
                sheet.set_column(0, 0, 13)
                sheet.write_string(self.row_pos, 0, _('Invoice date'), self.format_header)
                sheet.set_column(1, 1, 18)
                sheet.write_string(self.row_pos, 1, _('Invoice number'), self.format_header)
                sheet.set_column(2, 2, 20)
                sheet.write_string(self.row_pos, 2, _('Supplier Invoice'), self.format_header)
                sheet.set_column(3, 3, 55)
                sheet.write_string(self.row_pos, 3, _('Company'), self.format_header)
                sheet.set_column(4, 4, 15)
                sheet.write_string(self.row_pos, 4, _('VAT'), self.format_header)
                sheet.set_column(5, 5, 30)
                sheet.write_string(self.row_pos, 5, _('Code'), self.format_header)
                sheet.set_column(6, 6, 15)
                sheet.write_string(self.row_pos, 6, _('Base'), self.format_header)
                sheet.set_column(7, 7, 15)
                sheet.write_string(self.row_pos, 7, _('Type'), self.format_header)
                sheet.set_column(8, 8, 15)
                sheet.write_string(self.row_pos, 8, _('Cuote'), self.format_header)
                sheet.set_column(9, 9, 15)
                sheet.write_string(self.row_pos, 9, _('Total'), self.format_header)

        # To next row
        self.row_pos += 1

    def _generate_report_content(self, report_data, objects):
        print("holas")

    def generate_xlsx_report(self, workbook, data, objects):
        # Initial row
        self.row_pos = 0
        # Load formats to workbook
        self._define_formats(workbook)
        # Set report name
        report_name = _('VAT Book invoices issued')
        self.sheets = []
        self.sheets.append(workbook.add_worksheet(_('Invoices Issued')))
        self.sheets.append(workbook.add_worksheet(_('Invoices Received')))
        self.sheets.append(workbook.add_worksheet(_('Rectification Issued Invoices')))
        self.sheets.append(workbook.add_worksheet(_('Rectification Received Invoices')))
        self._write_report_title(report_name)
        self._write_report_attributes(objects)
        # Set headers
        self._set_headers()
        # Generate data
        initial_row = self.row_pos
        # account move lines
        for sheet in self.sheets:
            self.row_pos = initial_row
            if sheet.index == 0:
                invoices = objects.issued_invoice_ids
            elif sheet.index == 1:
                invoices = objects.received_invoice_ids
            elif sheet.index == 2:
                invoices = objects.rectification_issued_invoice_ids
            else:
                invoices = objects.rectification_received_invoice_ids

            for line in invoices:
                # import pdb; pdb.set_trace()
                if sheet.index == 0:
                    date_time = datetime.strptime(line.invoice_date, '%Y-%m-%d')
                    sheet.write_datetime(self.row_pos, 0, date_time, self.date_format)
                    sheet.write_string(self.row_pos, 1, line.invoice_id.number or '')
                    sheet.write_string(self.row_pos, 2, line.partner_id.name or '')
                    sheet.write_string(self.row_pos, 3, line.vat_number or '')
                    # sheet.write_string(self.row_pos, 4, line.base or '')
                    # number_taxes = 0
                    for tax in line.tax_line_issued_ids:
                        # if number_taxes != 0:
                        sheet.write_string(self.row_pos, 4, tax.name, self.num_format)
                        sheet.write_number(self.row_pos, 5, tax.amount_without_tax, self.num_format)
                        sheet.write_number(self.row_pos, 6, tax.tax_percent , self.porcentaje_format)
                        sheet.write_number(self.row_pos, 7, tax.tax_amount , self.num_format)
                        sheet.write_number(self.row_pos, 8, line.total, self.num_format)
                        self.row_pos = self.row_pos + 1
                elif sheet.index == 1:
                    date_time = datetime.strptime(line.invoice_date, '%Y-%m-%d')
                    sheet.write_datetime(self.row_pos, 0, date_time, self.date_format)
                    sheet.write_string(self.row_pos, 1, line.invoice_id.number or '')
                    sheet.write_string(self.row_pos, 2, line.invoice_id.reference or line.invoice_id.number)
                    sheet.write_string(self.row_pos, 3, line.partner_id.name or '')
                    sheet.write_string(self.row_pos, 4, line.vat_number or '')
                    # sheet.write_string(self.row_pos, 4, line.base or '')
                    # number_taxes = 0
                    for tax in line.tax_lines_received_ids:
                        # if number_taxes != 0:
                        sheet.write_string(self.row_pos, 5, tax.name, self.num_format)
                        sheet.write_number(self.row_pos, 6, tax.amount_without_tax, self.num_format)
                        sheet.write_number(self.row_pos, 7, tax.tax_percent , self.porcentaje_format)
                        sheet.write_number(self.row_pos, 8, tax.tax_amount , self.num_format)
                        sheet.write_number(self.row_pos, 9, line.total, self.num_format)
                        self.row_pos = self.row_pos + 1
                elif sheet.index == 2:
                    date_time = datetime.strptime(line.invoice_date, '%Y-%m-%d')
                    sheet.write_datetime(self.row_pos, 0, date_time, self.date_format)
                    sheet.write_string(self.row_pos, 1, line.invoice_id.number or '')
                    sheet.write_string(self.row_pos, 2, line.partner_id.name or '')
                    sheet.write_string(self.row_pos, 3, line.vat_number or '')
                    # sheet.write_string(self.row_pos, 4, line.base or '')
                    # number_taxes = 0
                    for tax in line.tax_lines_rectification_issued_ids:
                        # if number_taxes != 0:
                        sheet.write_string(self.row_pos, 4, tax.name, self.num_format)
                        sheet.write_number(self.row_pos, 5, tax.amount_without_tax, self.num_format)
                        sheet.write_number(self.row_pos, 6, tax.tax_percent , self.porcentaje_format)
                        sheet.write_number(self.row_pos, 7, tax.tax_amount , self.num_format)
                        sheet.write_number(self.row_pos, 8, line.total, self.num_format)
                        self.row_pos = self.row_pos + 1
                else:
                    date_time = datetime.strptime(line.invoice_date, '%Y-%m-%d')
                    sheet.write_datetime(self.row_pos, 0, date_time, self.date_format)
                    sheet.write_string(self.row_pos, 1, line.invoice_id.number or '')
                    sheet.write_string(self.row_pos, 2, line.partner_id.name or '')
                    sheet.write_string(self.row_pos, 3, line.vat_number or '')
                    # sheet.write_string(self.row_pos, 4, line.base or '')
                    # number_taxes = 0
                    for tax in line.tax_lines_rectification_received_ids:
                        # if number_taxes != 0:
                        sheet.write_string(self.row_pos, 4, tax.name, self.num_format)
                        sheet.write_number(self.row_pos, 5, tax.amount_without_tax, self.num_format)
                        sheet.write_number(self.row_pos, 6, tax.tax_percent , self.porcentaje_format)
                        sheet.write_number(self.row_pos, 7, tax.tax_amount , self.num_format)
                        sheet.write_number(self.row_pos, 8, line.total, self.num_format)
                        self.row_pos = self.row_pos + 1

            # self._generate_report_content(data, objects)
            # Sumary Section
            self.row_pos += 2
            if sheet.index == 0:
                sheet.merge_range(
                    self.row_pos, 0, self.row_pos, 8, _('Summary invoices issued'), self.format_header
                )
            elif sheet.index == 1:
                sheet.merge_range(
                    self.row_pos, 0, self.row_pos, 8, _('Summary invoices received'), self.format_header
                )
            elif sheet.index == 2:
                sheet.merge_range(
                    self.row_pos, 0, self.row_pos, 8, _('Summary rectification issued invoices'), self.format_header
                )
            else:
                sheet.merge_range(
                    self.row_pos, 0, self.row_pos, 8, _('Summary rectification received invoices'), self.format_header
                )

            self.row_pos += 2
            #Summary headers
            sheet.merge_range(self.row_pos, 0, self.row_pos, 4, _('Code'), self.format_header)
            sheet.write_string(self.row_pos, 5, _('Base'), self.format_header)
            sheet.write_string(self.row_pos, 6, _('Cuote'), self.format_header)
            sheet.write_string(self.row_pos, 7, _('Type'), self.format_header)
            sheet.write_string(self.row_pos, 8, _('Total'), self.format_header)
            self.row_pos += 1
            #Summary data
            if sheet.index == 0:
                for s in objects.issued_tax_summary:
                        sheet.merge_range(self.row_pos, 2, self.row_pos, 4, s.tax_code_id.name)
                        sheet.write_number(self.row_pos, 5, s.sum_base_amount, self.num_format)
                        sheet.write_number(self.row_pos, 6, s.sum_tax_amount, self.num_format)
                        sheet.write_number(self.row_pos, 7, s.tax_percent, self.porcentaje_format)
                        sheet.write_number(self.row_pos, 8, s.sum_tax_amount + s.sum_base_amount, self.num_format)
                        self.row_pos += 1
                sheet.write_number(self.row_pos, 5, objects.amount_without_tax_issued, self.format_total)
                sheet.write_number(self.row_pos, 6, objects.amount_tax_issued, self.format_total)
                sheet.write_number(self.row_pos, 8, objects.amount_total_issued, self.format_total)
            elif sheet.index == 1:
                for s in objects.received_tax_summary:
                        sheet.merge_range(self.row_pos, 2, self.row_pos, 4, s.tax_code_id.name)
                        sheet.write_number(self.row_pos, 5, s.sum_base_amount, self.num_format)
                        sheet.write_number(self.row_pos, 6, s.sum_tax_amount, self.num_format)
                        sheet.write_number(self.row_pos, 7, s.tax_percent, self.porcentaje_format)
                        sheet.write_number(self.row_pos, 8, s.sum_tax_amount + s.sum_base_amount, self.num_format)
                        self.row_pos += 1
                sheet.write_number(self.row_pos, 5, objects.amount_without_tax_received, self.format_total)
                sheet.write_number(self.row_pos, 6, objects.amount_tax_received, self.format_total)
                sheet.write_number(self.row_pos, 8, objects.amount_total_received, self.format_total)
            elif sheet.index == 2:
                for s in objects.rectification_issued_tax_summary:
                        sheet.merge_range(self.row_pos, 2, self.row_pos, 4, s.tax_code_id.name)
                        sheet.write_number(self.row_pos, 5, s.sum_base_amount, self.num_format)
                        sheet.write_number(self.row_pos, 6, s.sum_tax_amount, self.num_format)
                        sheet.write_number(self.row_pos, 7, s.tax_percent, self.porcentaje_format)
                        sheet.write_number(self.row_pos, 8, s.sum_tax_amount + s.sum_base_amount, self.num_format)
                        self.row_pos += 1
                sheet.write_number(self.row_pos, 5, objects.amount_without_tax_rectification_issued, self.format_total)
                sheet.write_number(self.row_pos, 6, objects.amount_tax_rectification_issued, self.format_total)
                sheet.write_number(self.row_pos, 8, objects.amount_total_rectification_issued, self.format_total)
            else:
                for s in objects.rectification_received_tax_summary:
                        sheet.merge_range(self.row_pos, 2, self.row_pos, 4, s.tax_code_id.name)
                        sheet.write_number(self.row_pos, 5, s.sum_base_amount, self.num_format)
                        sheet.write_number(self.row_pos, 6, s.sum_tax_amount, self.num_format)
                        sheet.write_number(self.row_pos, 7, s.tax_percent, self.porcentaje_format)
                        sheet.write_number(self.row_pos, 8, s.sum_tax_amount + s.sum_base_amount, self.num_format)
                        self.row_pos += 1
                sheet.write_number(self.row_pos, 5, objects.amount_without_tax_rectification_received, self.format_total)
                sheet.write_number(self.row_pos, 6, objects.amount_tax_rectification_received, self.format_total)
                sheet.write_number(self.row_pos, 8, objects.amount_total_rectification_received, self.format_total)


if ReportXlsx != object:
    IvaXlsx(
        'report.vat_book_invoices_issued_xls',
        'l10n.es.vat.book', parser=report_sxw.rml_parse
    )
