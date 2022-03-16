
from odoo import api, fields, models, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.onchange('payment_mode_id')
    def _onchange_payment_mode(self):
        self.cancel_payment_transactions()

    def cancel_payment_transactions(self):
        for record in self:
            for transaction in record.transaction_ids:
                for invoice in record.invoice_ids:
                    if invoice.state != 'paid':
                        transaction.unlink()

