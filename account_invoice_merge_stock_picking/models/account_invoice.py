# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, api


class AccountInvoice(models.Model):

    _inherit = 'account.invoice'

    @api.multi
    def do_merge(self, keep_references=True, date_invoice=False):
        inv_model = self.env['account.invoice']
        inv_info, inv_line_info = super(AccountInvoice, self).do_merge(
            keep_references=keep_references, date_invoice=date_invoice)
        picks = self.env['stock.picking']
        for inv_id in inv_info:
            inv = inv_model.browse(inv_id)
            src_invs = inv_model.browse(inv_info[inv_id])
            pickings = src_invs.mapped('picking_ids')
            picks += pickings
            inv.picking_ids = pickings
            pickings.write({'invoice_state': 'invoiced'})
        return inv_info, inv_line_info
