
from odoo import api, fields, models, _


class PaymentAcquirer(models.Model):
    _inherit = 'payment.acquirer'

    @api.depends('journal_id', 'journal_id.inbound_payment_method_ids')
    def _get_journal_payment_methods(self):
        self.ensure_one()
        if self.website_published:
            payment_modes = self.env['account.payment.mode'].search([
                ('payment_method_id', 'in',
                 self.journal_id.inbound_payment_method_ids.ids)
            ])
            return payment_modes
