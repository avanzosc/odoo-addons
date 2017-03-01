# -*- coding: utf-8 -*-
# (c) 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api
from openerp.addons import decimal_precision as dp


class PurchaseRequisition(models.Model):
    _inherit = 'purchase.requisition'

    @api.multi
    @api.depends('sale_order_id', 'sale_order_id.amount_total',
                 'sale_order_id.state')
    def _compute_sale_amount_total(self):
        for p in self:
            p.sale_amount_total = 0
            if p.sale_order_id.state not in ('draft', 'cancel'):
                p.sale_amount_total = p.sale_order_id.amount_total

    @api.multi
    @api.depends('line_ids', 'line_ids.total_cost')
    def _compute_purchase_amount_total(self):
        for p in self:
            p.purchase_amount_total = sum(self.line_ids.mapped('total_cost'))

    @api.multi
    @api.depends('sale_amount_total', 'purchase_amount_total')
    def _compute_margin(self):
        for p in self:
            p.margin = 0
            if p.sale_amount_total and p.purchase_amount_total:
                p.margin = 1 - (p.purchase_amount_total / p.sale_amount_total)

    sale_amount_total = fields.Float(
        string='Total sale', digits=dp.get_precision('Account'),
        compute='_compute_sale_amount_total', store=True)
    purchase_amount_total = fields.Float(
        string='Total purchase', digits=dp.get_precision('Account'),
        compute='_compute_purchase_amount_total', store=True)
    margin = fields.Float(
        string='Margin', digits=dp.get_precision('Product UoS'), default=0.000,
        compute='_compute_margin', store=True)


class PurchaseRequisitionLine(models.Model):
    _inherit = 'purchase.requisition.line'

    @api.multi
    @api.depends('product_qty', 'psp_unit')
    def _compute_psp_subtotal(self):
        for line in self:
            line.psp_subtotal = line.psp_unit * line.product_qty

    @api.onchange('margin', 'unit_cost')
    def onchange_margin(self):
        for line in self.filtered(lambda x: x.margin and x.unit_cost):
            line.psp_unit = line.unit_cost / (1 - line.margin)

    @api.multi
    @api.depends('sale_order_line_id', 'sale_order_line_id.price_unit')
    def _compute_psp_unit(self):
        for line in self:
            line.psp_unit = line.sale_order_line_id.price_unit

    @api.multi
    def _inverse_psp_unit(self):
        self.ensure_one()
        self.sale_order_line_id.price_unit = self.psp_unit

    margin = fields.Float(
        string='Margin', digits=dp.get_precision('Product UoS'), default=0.000,
        help='For example, you must put a 0.014 for a margin of 1.4%')
    psp_unit = fields.Float(
        string='PSP Unit', digits=dp.get_precision('Product Price'),
        compute='_compute_psp_unit',
        inverse='_inverse_psp_unit', store=True)
    psp_subtotal = fields.Float(
        string='PSP Subtotal', digits=dp.get_precision('Product Price'),
        compute='_compute_psp_subtotal')
