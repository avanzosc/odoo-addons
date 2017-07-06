# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - Avanzosc S.L.
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, api


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
