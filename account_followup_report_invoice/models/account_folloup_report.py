# Copyright 2021 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, _


class AccountFollowupReport(models.AbstractModel):
    _inherit = 'account.followup.report'

    def _get_columns_name(self, options):
        headers = super(AccountFollowupReport, self)._get_columns_name(options)
        for header in headers:
            if not header:
                header.update(
                    {'name': _('Invoice'),
                     'style': 'text-align:center; white-space:nowrap;'})
        return headers

    def _get_lines(self, options, line_id=None):
        lines = super(AccountFollowupReport, self)._get_lines(
            options, line_id=line_id)
        for line in lines:
            if 'invoice_id' in line and line.get('invoice_id', False):
                invoice = self.env['account.invoice'].browse(
                    line.get('invoice_id'))
                line['name'] = invoice.number
        return lines
