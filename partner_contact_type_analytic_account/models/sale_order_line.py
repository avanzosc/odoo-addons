# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _prepare_invoice_line(self, **optional_values):
        values = super(SaleOrderLine, self)._prepare_invoice_line(
            **optional_values)
        if self.order_id.analytic_account_id:
            values['analytic_account_id'] = (
                self.order_id.analytic_account_id.id)
        return values
