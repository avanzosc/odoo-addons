# -*- coding: utf-8 -*-
# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, api


class AccountVoucher(models.Model):
    _inherit = 'account.voucher'

    @api.model
    def voucher_move_line_create(self, voucher_id, line_total, move_id,
                                 company_currency, current_currency):
        line_obj = self.env['account.move.line']
        tot_line, rec_list_ids = super(
            AccountVoucher, self).voucher_move_line_create(
            voucher_id, line_total, move_id, company_currency,
            current_currency)
        move_line_ids = []
        m_line = self.env['account.move']
        inumbers = ''
        for list in rec_list_ids:
            if list and list[0] and list[1]:
                invoice, m_line = self.put_invoice_ref_in_account_move_line(
                    line_obj.browse(list[0]), line_obj.browse(list[1]))
                move_line_ids.append(list[0])
                inumbers = (invoice.number if not inumbers else
                            u"{}, {}".format(inumbers, invoice.number))
        if move_line_ids and m_line:
            cond = [('id', 'not in', move_line_ids),
                    ('move_id', '=', m_line.id)]
            amovel = self.env['account.move.line'].search(cond, limit=1)
            if amovel:
                amovel.name = u"{} {}".format(inumbers, amovel.name)
        return (tot_line, rec_list_ids)

    @api.multi
    def put_invoice_ref_in_account_move_line(self, paymentline, validateline):
        cond = [('move_id', '=', validateline.move_id.id)]
        invoice = self.env['account.invoice'].search(cond, limit=1)
        if invoice:
            paymentline.name = u"{} {}".format(invoice.number,
                                               paymentline.name)
        return invoice, paymentline.move_id

    @api.model
    def writeoff_move_line_get(self, voucher_id, line_total, move_id, name,
                               company_currency, current_currency,
                               local_context):
        res = super(
            AccountVoucher,
            self.with_context(local_context)).writeoff_move_line_get(
            voucher_id, line_total, move_id, name, company_currency,
            current_currency)
        move = self.env['account.move'].browse(move_id)
        if res and move.line_id:
            pos = move.line_id[0].name.find(" /")
            lit = move.line_id[0].name[:pos]
            res['name'] = u"{} {}".format(lit, res.get('name'))
        return res
