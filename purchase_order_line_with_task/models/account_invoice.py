# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, api


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    def _prepare_invoice_line_from_po_line(self, line):
        data = super(
            AccountInvoice, self)._prepare_invoice_line_from_po_line(line)
        if line.allowed_task_ids:
            data['allowed_task_ids'] = [(6, 0, line.allowed_task_ids.ids)]
        if line.task_id:
            data['task_id'] = line.task_id.id
        return data

    @api.model
    def invoice_line_move_line_get(self):
        result = super(AccountInvoice, self).invoice_line_move_line_get()
        if result:
            for line in result:
                if line.get('invl_id', False):
                    invoice_line = self.env['account.invoice.line'].browse(
                        line.get('invl_id'))
                    if invoice_line.allowed_task_ids:
                        line['allowed_task_ids'] = [
                            (6, 0, invoice_line.allowed_task_ids.ids)]
                    if invoice_line.task_id:
                        line['task_id'] = invoice_line.task_id.id
        return result
