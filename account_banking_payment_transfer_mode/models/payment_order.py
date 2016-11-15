# -*- coding: utf-8 -*-
# © 2016 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, api


class PaymentOrder(models.Model):
    '''
    Enable extra states for payment exports
    '''
    _inherit = 'payment.order'

    @api.multi
    def _prepare_move_line_transfer_account(
            self, amount, move, bank_payment_lines, labels):
        vals = super(PaymentOrder, self)._prepare_move_line_transfer_account(
            amount, move, bank_payment_lines, labels)
        vals['manual_payment_mode'] = self.mode.transfer_payment_mode.id
        return vals
