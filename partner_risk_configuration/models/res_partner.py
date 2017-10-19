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
                 'parent_id', 'parent_id.unified_risk',
                 'invoice_ids.amount_total', 'invoice_ids.residual',
                 'invoice_ids.company_id.invoice_unpaid_margin')
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
            partner.risk_invoice_draft = sum(invoices.mapped('amount_total'))
            invoices = invoices_out.filtered(
                lambda x: x.state == 'open' and x.date_due >= max_date)
            partner.risk_invoice_open = sum(invoices.mapped('residual'))
            invoices = invoices_out.filtered(
                lambda x: x.state == 'open' and x.date_due < max_date)
            partner.risk_invoice_unpaid = sum(invoices.mapped('residual'))

    @api.multi
    @api.depends('sale_order_ids', 'sale_order_ids.invoice_pending_amount',
                 'child_ids.sale_order_ids', 'unified_risk', 'parent_id',
                 'parent_id.unified_risk', 'sale_order_ids.state',
                 'child_ids.sale_order_ids.invoice_pending_amount')
    def _compute_risk_sale_order(self):
        customers = self.filtered('customer')
        partners = customers | customers.mapped('child_ids')
        orders_group = self.env['sale.order'].read_group(
            [('state', 'not in', ['draft', 'sent', 'cancel', 'done']),
             ('partner_id', 'in', partners.ids)],
            ['partner_id', 'invoice_pending_amount'],
            ['partner_id'])
        for partner in customers:
            partner_ids = (partner.commercial_partner_id.unified_risk and
                           (partner | partner.mapped('child_ids')).ids or
                           [partner.id])
            partner.risk_sale_order = sum(
                [x['invoice_pending_amount']
                 for x in orders_group if x['partner_id'][0] in partner_ids])
