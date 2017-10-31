# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class ResPartner(models.Model):

    _inherit = 'res.partner'

    @api.model
    def _get_default_unified_risk(self):
        return self.env['account.config.settings'
                        ].get_unified_risk_default_value()

    unified_risk = fields.Boolean(string="Unified risk in parent",
                                  default=_get_default_unified_risk)

    @api.onchange('unified_risk')
    @api.multi
    def onchange_unified_risk(self):
        self.ensure_one()
        self.mapped('child_ids').write({'unified_risk': self.unified_risk})

    @api.multi
    def get_risk_partner(self):
        self.ensure_one()
        return self.parent_id.unified_risk and self.parent_id or self

    @api.multi
    @api.depends('invoice_ids', 'invoice_ids.state', 'unified_risk',
                 'parent_id', 'parent_id.unified_risk', 'invoice_ids.date_due',
                 'invoice_ids.amount_total', 'invoice_ids.residual',
                 'invoice_ids.company_id.invoice_unpaid_margin',
                 'child_ids', 'child_ids.invoice_ids',
                 'child_ids.invoice_ids.state',
                 'child_ids.invoice_ids.amount_total',
                 'child_ids.invoice_ids.residual',
                 'child_ids.invoice_ids.company_id.invoice_unpaid_margin',
                 'invoice_ids.currency_id', 'child_ids.invoice_ids.company_id',
                 'child_ids.invoice_ids.currency_id',
                 'invoice_ids.company_id', 'child_ids.invoice_ids.date_due',
                 'invoice_ids.company_id.currency_id',
                 'child_ids.invoice_ids.company_id.currency_id')
    def _compute_risk_invoice(self):
        invoice_model = self.env['account.invoice']
        max_date = self._max_risk_date_due()
        for partner in self:
            commercial_partner = partner.commercial_partner_id
            invoices_out = (
                commercial_partner.unified_risk and invoice_model.search(
                    [('type', '=', 'out_invoice'),
                     ('partner_id', 'child_of', commercial_partner.id)]) or
                partner.invoice_ids.filtered(lambda x: x.type == 'out_invoice')
                )
            invoices = invoices_out.filtered(
                lambda x: x.state in ['draft', 'proforma', 'proforma2'])
            risk_invoice_draft = 0
            for invoice in invoices:
                if invoice.currency_id != invoice.company_id.currency_id:
                    risk_invoice_draft += invoice.currency_id.with_context(
                        date=invoice.date_invoice).compute(
                            invoice.amount_total,
                            invoice.company_id.currency_id)
                else:
                    risk_invoice_draft += invoice.amount_total
            partner.risk_invoice_draft = risk_invoice_draft
            invoices = invoices_out.filtered(
                lambda x: x.state == 'open' and x.date_due >= max_date)
            risk_invoice_open = 0
            for invoice in invoices:
                if invoice.currency_id != invoice.company_id.currency_id:
                    risk_invoice_open += invoice.currency_id.with_context(
                        date=invoice.date_invoice).compute(
                            invoice.residual, invoice.company_id.currency_id)
                else:
                    risk_invoice_open += invoice.residual
            partner.risk_invoice_open = risk_invoice_open
            invoices = invoices_out.filtered(
                lambda x: x.state == 'open' and x.date_due < max_date)
            risk_invoice_unpaid = 0
            for invoice in invoices:
                if invoice.currency_id != invoice.company_id.currency_id:
                    risk_invoice_unpaid += invoice.currency_id.with_context(
                        date=invoice.date_invoice).compute(
                            invoice.residual, invoice.company_id.currency_id)
                else:
                    risk_invoice_unpaid += invoice.residual
            partner.risk_invoice_unpaid = risk_invoice_unpaid

    @api.multi
    @api.depends('sale_order_ids', 'sale_order_ids.invoice_pending_amount',
                 'child_ids.sale_order_ids', 'unified_risk', 'parent_id',
                 'parent_id.unified_risk', 'sale_order_ids.state',
                 'child_ids.sale_order_ids.state',
                 'child_ids.sale_order_ids.invoice_pending_amount',
                 'sale_order_ids.pricelist_id.currency_id',
                 'sale_order_ids.pricelist_id', 'sale_order_ids.company_id',
                 'sale_order_ids.company_id.currency_id',
                 'child_ids.sale_order_ids.pricelist_id.currency_id',
                 'child_ids.sale_order_ids.pricelist_id',
                 'child_ids.sale_order_ids.company_id',
                 'child_ids.sale_order_ids.company_id.currency_id')
    def _compute_risk_sale_order(self):
        for partner in self.filtered('customer'):
            partner_ids = (partner.commercial_partner_id.unified_risk and
                           (partner | partner.mapped('child_ids')).ids or
                           [partner.id])
            orders = self.env['sale.order'].search(
                [('state', 'not in', ['draft', 'sent', 'cancel', 'done']),
                 ('partner_id', 'in', partner_ids)])
            sale_risk_amount = 0
            for sale in orders:
                company_currency = sale.company_id.currency_id
                sale_currency = sale.pricelist_id.currency_id
                if sale_currency != company_currency:
                    sale_risk_amount += sale_currency.with_context(
                        date=sale.date_order).compute(
                            sale.invoice_pending_amount, company_currency)
                else:
                    sale_risk_amount += sale.invoice_pending_amount
            partner.risk_sale_order = sale_risk_amount
