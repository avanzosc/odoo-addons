# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - Avanzosc S.L.
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, fields, models


class AccountInvoice(models.Model):

    _inherit = 'account.invoice'

    @api.multi
    @api.depends(
        'move_id.line_id.reconcile_id.line_id',
        'move_id.line_id.reconcile_partial_id.line_partial_ids',
        'move_id.line_id.reconcile_id.line_id.date',
        'move_id.line_id.reconcile_partial_id.line_partial_ids.date')
    def _compute_payment_date(self):
        for invoice in self:
            move_lines = invoice.mapped('move_id.line_id').filtered(
                lambda x: x.account_id == invoice.account_id)
            reconcile_lines = self.env['account.move.line']
            reconcile_lines |= move_lines.mapped('reconcile_id.line_id')
            reconcile_lines |= move_lines.mapped(
                'reconcile_partial_id.line_partial_ids')
            reconcile_lines -= move_lines
            invoice.payment_date = (
                reconcile_lines and min(reconcile_lines.mapped('date')) or
                False)

    payment_date = fields.Date(compute='_compute_payment_date',
                               string='Payment Date', store=True)

    @api.multi
    def onchange_partner_id(
            self, type, partner_id, date_invoice=False,
            payment_term=False, partner_bank_id=False, company_id=False):
        res = super(AccountInvoice, self).onchange_partner_id(
            type, partner_id, date_invoice=date_invoice,
            payment_term=payment_term, partner_bank_id=partner_bank_id,
            company_id=company_id)
        p = self.env['res.partner'].browse(partner_id or False)
        domain = res.setdefault('domain', {})
        if type in ('in_invoice', 'out_refund'):
            bank_ids = p.commercial_partner_id.bank_ids
            if bank_ids:
                domain['partner_bank_id'] = [('id', 'in', bank_ids.ids)]
            else:
                domain['partner_bank_id'] = [
                    ('partner_id', '=', p.commercial_partner_id.id)]
        return res
