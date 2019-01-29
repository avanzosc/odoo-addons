# -*- coding: utf-8 -*-
# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, api


class AccountVoucher(models.Model):
    _inherit = 'account.voucher'

    @api.multi
    def button_proforma_voucher(self):
        res = super(AccountVoucher, self).button_proforma_voucher()
        if (self.env.context.get('active_model', False) and
            self.env.context.get('active_model') == 'account.invoice' and
                self.env.context.get('invoice_id', False)):
            vouchers = self.filtered(lambda c: c.move_id)
            if vouchers:
                vouchers.put_invoice_ref_in_account_move_line()
        return res

    @api.multi
    def put_invoice_ref_in_account_move_line(self):
        invoice = self.env['account.invoice'].browse(
            self.env.context.get('invoice_id'))
        for voucher in self:
            for line in voucher.move_id.line_id:
                line.name = u"{} {}".format(invoice.number, line.name)
