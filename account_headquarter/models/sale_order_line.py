# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _prepare_invoice_line(self, **optional_values):
        values = super(SaleOrderLine, self)._prepare_invoice_line(
            **optional_values)
        if self.order_id.headquarter_id:
            values['headquarter_id'] = self.order_id.headquarter_id.id
            if 'account_id' in values and values.get('account_id', False):
                account = self.env['account.account'].browse(
                    values.get('account_id'))
                if account:
                    without_headquarter = (
                        account.group_id._find_account_group_headquarter())
                    if without_headquarter:
                        values['headquarter_id'] = False
        return values
