# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, models


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    def _prepare_invoice_line_from_po_line(self, line):
        data = super(
            AccountInvoice, self)._prepare_invoice_line_from_po_line(line)
        if line.task_id:
            data["task_id"] = line.task_id.id
        return data
