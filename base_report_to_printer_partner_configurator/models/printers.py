# -*- coding: utf-8 -*-
# © 2015 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, models


class PrintingPrinter(models.Model):
    _inherit = 'printing.printer'

    @api.multi
    def print_document(self, report, content, format, copies=1):
        try:
            copies = copies
        except:
            pass
        return super(PrintingPrinter, self).print_document(
            report, content, format, copies=copies)
