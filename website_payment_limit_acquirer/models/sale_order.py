
from odoo import api, fields, models, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    transaction_count = fields.Integer(
        string='Transactions Count',
        compute='_get_transactions',
        readonly=True)

    def _get_transactions(self):
        for record in self:
            record.transaction_count = len(record.transaction_ids)

    # @api.onchange('payment_mode_id')
    # def _onchange_payment_mode(self):
    #     self.cancel_payment_transactions()

    def cancel_payment_transactions(self):
        for record in self:
            for transaction in record.transaction_ids:
                for invoice in record.invoice_ids:
                    if invoice.state != 'paid':
                        transaction.unlink()

    @api.multi
    def action_show_related_transactions(self):
        self.ensure_one()
        transaction_ids = self.transaction_ids.ids
        return {
            "type": "ir.actions.act_window",
            "res_model": "payment.transaction",
            "views": [[False, "tree"], [False, "form"]],
            "domain": [("id", "in", transaction_ids)],
            "name": "Related Transactions",
        }
