# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, models, exceptions, _


class AccountAnalyticLine(models.Model):

    _inherit = 'account.analytic.line'

    @api.multi
    def invoice_cost_create_by_partner(self, data=None):
        invoice_obj = self.env['account.invoice']
        invoice_line_obj = self.env['account.invoice.line']
        invoices = []
        data = data or {}
        invoice_grouping = {}
        currency_id = False
        accounts = self.mapped('account_id').filtered(
            lambda x: not x.partner_id or not x.pricelist_id.currency_id)
        if accounts:
            raise exceptions.Warning(
                _('Error!, Contract incomplete. Please fill in the Customer '
                  'and Pricelist fields for %s.') %
                (','.join(accounts.mapped('name'))))
        lines = self.filtered(lambda x: not x.to_invoice)
        if lines:
            raise exceptions.Warning(
                _('Error! Trying to invoice non invoiceable line for %s.') %
                (','.join(lines.mapped('product_id.name'))))
        for line in self:
            key = (line.account_id.partner_id.id,
                   line.account_id.company_id.id,
                   line.account_id.pricelist_id.currency_id.id)
            invoice_grouping.setdefault(key, []).append(line)

        for (key_id, company_id, currency_id), analytic_lines in \
                invoice_grouping.items():
            partner = analytic_lines[0].account_id.partner_id
            curr_invoice = self._prepare_cost_invoice(
                partner, company_id, currency_id, analytic_lines)
            last_invoice = invoice_obj.with_context(
                lang=partner.lang, force_company=company_id,
                company_id=company_id).create(curr_invoice)
            invoices.append(last_invoice.id)
            invoice_lines_grouping = {}
            for analytic_line in analytic_lines:
                key = (analytic_line.product_id.id,
                       analytic_line.product_uom_id.id,
                       analytic_line.user_id.id,
                       analytic_line.to_invoice.id,
                       analytic_line.account_id,
                       analytic_line.journal_id.type)
                invoice_lines_grouping.setdefault(key, []
                                                  ).append(analytic_line)
            for (product_id, uom, user_id, factor_id,
                    analytic_line.account_id, journal_type), \
                    lines_to_invoice in invoice_lines_grouping.items():
                curr_invoice_line = self.with_context(
                    lang=partner.lang, force_company=company_id,
                    company_id=company_id)._prepare_cost_invoice_line(
                    last_invoice.id, product_id, uom, user_id, factor_id,
                    analytic_line.account_id, lines_to_invoice, journal_type,
                    data)
                invoice_line_obj.create(curr_invoice_line)
            lines = self.env['account.analytic.line']
            for line in analytic_lines:
                lines |= line
            lines.write({'invoice_id': last_invoice.id})
            last_invoice.button_reset_taxes()
        return invoices

    @api.multi
    def invoice_cost_create(self, data=None):
        if not self.env['ir.config_parameter'].search(
                [('key', '=', 'invoice_by_partner')]):
            return super(AccountAnalyticLine, self
                         ).invoice_cost_create(data=data)
        else:
            return self.invoice_cost_create_by_partner(data=data)
