# -*- coding: utf-8 -*-

from openerp import models
from openerp.report import report_sxw


class VatBookInvoicesSummary(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context):
        super(VatBookInvoicesSummary, self).__init__(
            cr, uid, name, context)


class WrappedVatBookSummary(models.AbstractModel):
    _name = 'report.l10n_es_vat_book.tmp_report_vat_book_summary'
    _inherit = 'report.abstract_report'
    _template = 'l10n_es_vat_book.tmp_report_vat_book_summary'
    _wrapped_report_class = VatBookInvoicesSummary
