# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
# Copyright (c) 2019 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.

from odoo import fields, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    client_order_ref = fields.Char(string='Customer Reference', copy=False)

    def write(self, vals):
        if 'sale_loop' in self.env.context and 'client_order_ref' in vals:
            del vals['client_order_ref']
        if 'client_order_ref' in vals:
            sale_orders = self.mapped(
                'invoice_line_ids.sale_line_ids.order_id')
            sale_orders.with_context(sale_loop=True).write(
                {'client_order_ref': vals['client_order_ref']})
        return super().write(vals)
