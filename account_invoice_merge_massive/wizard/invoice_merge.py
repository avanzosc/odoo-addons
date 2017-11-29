# -*- coding: utf-8 -*-
# Copyright 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, api


class InvoiceMerge(models.TransientModel):
    _inherit = "invoice.merge"

    @api.model
    def _dirty_check(self):
        if self.env.context.get('active_model') == 'account.invoice':
            group_invoices = self._group_invoices_to_treat()
            for invoices in group_invoices:
                res = super(
                    InvoiceMerge,
                    self.with_context(active_ids=invoices.ids))._dirty_check()
        else:
            res = super(InvoiceMerge, self)._dirty_check()
        return res

    @api.multi
    def merge_invoices(self):
        invoice_ids = []
        group_invoices = self._group_invoices_to_treat()
        for invoices in group_invoices:
            res = super(
                InvoiceMerge,
                self.with_context(active_ids=invoices.ids)).merge_invoices()
            domain = res.get('domain', [])
            for inv_ids in domain:
                if inv_ids[0] == 'id':
                    invoice_ids += inv_ids[2]
        res['domain'] = [('id', 'in', invoice_ids)]
        return res

    def _group_invoices_to_treat(self):
        all_invoices = self.env['account.invoice'].browse(
            self._context['active_ids'])
        sql = ("SELECT partner_id, account_id, company_id, type, "
               "       currency_id, journal_id, partner_bank_id "
               "FROM   account_invoice "
               "WHERE  state = 'draft' "
               "  AND  id in %s "
               "GROUP BY partner_id, account_id, company_id, type, "
               "        currency_id, journal_id, partner_bank_id ")
        cr = self.env.cr
        cr.execute(sql, (tuple(all_invoices.ids), ))
        res = cr.dictfetchall()
        tab = []
        for r in res:
            invoices = all_invoices.filtered(
                lambda x: x.partner_id.id == r.get('partner_id') and
                x.account_id.id == r.get('account_id') and
                x.company_id.id == r.get('company_id') and
                x.type == r.get('type') and
                x.currency_id.id == r.get('currency_id') and
                x.journal_id.id == r.get('journal_id') and
                ((r.get('partner_bank_id') is not None and
                  r.get('partner_bank_id') == x.partner_bank_id.id) or
                 (r.get('partner_bank_id') is None and not
                  x.partner_bank_id)))
            if len(invoices) > 1:
                tab.append(invoices)
        return tab
