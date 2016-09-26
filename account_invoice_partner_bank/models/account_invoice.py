# -*- coding: utf-8 -*-
# © 2016 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, api


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    payment_mode_id = fields.Many2one(
        comodel_name='payment.mode', string="Payment Mode",
        domain="[('type', '=', type)]")

    @api.multi
    @api.onchange('payment_mode_id', 'payment_mode_id.partner_bank', 'type',
                  'payment_mode_id.bank_id')
    def onchange_payment_mode(self):
        self.ensure_one()
        domain = []
        if self.payment_mode_id.partner_bank:
            self.partner_bank_id = self.partner_id.bank_ids[:1]
            domain += [('partner_id', '=', self.partner_id.id)]
        elif self.type == 'out_invoice' and self.payment_mode_id.bank_id:
            self.partner_bank_id = self.payment_mode_id.bank_id
            domain += [('partner_id.ref_companies', 'in',
                        [self.company_id.id])]
        return {'domain': {'partner_bank_id': domain}}
