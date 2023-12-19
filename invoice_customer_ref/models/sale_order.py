# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
# Copyright (c) 2019 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.

from odoo import api, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def write(self, vals):
        if 'invoice_loop' in self.env.context and 'client_order_ref' in vals:
            del vals['client_order_ref']
        if 'client_order_ref' in vals:
            invoices = self.mapped(
                'order_line.invoice_lines.invoice_id').filtered(
                    lambda r: r.type in ['out_invoice', 'out_refund'])
            invoices.with_context(invoice_loop=True).write(
                {'client_order_ref': vals['client_order_ref']})
        return super().write(vals)

    @api.multi
    def _prepare_invoice(self):
        res = super(SaleOrder, self)._prepare_invoice()
        if self.client_order_ref:
            res.update({'client_order_ref': self.client_order_ref})
        return res
