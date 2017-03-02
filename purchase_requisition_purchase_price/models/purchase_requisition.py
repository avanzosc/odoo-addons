# -*- coding: utf-8 -*-
# (c) 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api
from openerp.addons import decimal_precision as dp


class PurchaseRequisition(models.Model):
    _inherit = 'purchase.requisition'

    @api.model
    def _prepare_purchase_order_line(self, requisition, requisition_line,
                                     purchase_id, supplier):
        vals = super(PurchaseRequisition, self)._prepare_purchase_order_line(
            requisition, requisition_line, purchase_id, supplier)
        vals['prequisition_line_id'] = requisition_line.id
        return vals


class PurchaseRequisitionLine(models.Model):
    _inherit = 'purchase.requisition.line'

    @api.onchange('purchase_price', 'transportation_price')
    def onchange_purchase_price_transportation_price(self):
        for line in self:
            line._compute_total_cost()

    @api.multi
    @api.depends('purchase_price', 'transportation_price',
                 'total_cost', 'product_qty')
    def _compute_total_cost(self):
        for line in self:
            line.total_cost = line.purchase_price + line.transportation_price
            line.unit_cost = 0
            if line.total_cost and line.product_qty:
                line.unit_cost = line.total_cost / line.product_qty

    @api.multi
    @api.depends('purchase_line_ids', 'purchase_line_ids.price_unit',
                 'purchase_line_ids.product_qty')
    def _compute_purchase_price(self):
        for pline in self:
            pline.purchase_line_ids.write({
                'total_amount_used': False,
                'partial_amount_used': False})
            product_qty = pline.product_qty
            purchase_price = 0
            for line in pline.purchase_line_ids:
                if line.product_qty <= product_qty:
                    purchase_price += line.product_qty * line.price_unit
                    line.write({'total_amount_used': True})
                    product_qty -= line.product_qty
                else:
                    purchase_price += product_qty * line.price_unit
                    line.write({'partial_amount_used': True})
                    product_qty = 0
                if product_qty == 0:
                    break
            pline.purchase_price = purchase_price

    @api.multi
    def _inverse_purchase_price(self):
        return True

    standard_price = fields.Float(
        string='Cost Price', related='product_id.standard_price',
        digits=dp.get_precision('Product Price'))
    purchase_price = fields.Float(
        string='Purchase price', digits=dp.get_precision('Product Price'),
        compute='_compute_purchase_price',
        inverse='_inverse_purchase_price', store=True)
    transportation_price = fields.Float(
        string='Transportation', digits=dp.get_precision('Product Price'))
    total_cost = fields.Float(
        string='Total cost', compute='_compute_total_cost',
        digits=dp.get_precision('Product Price'), store=True)
    unit_cost = fields.Float(
        string='Unit cost', compute='_compute_total_cost',
        digits=dp.get_precision('Product Price'))
    purchase_line_ids = fields.One2many(
        string='Purchase order lines', comodel_name='purchase.order.line',
        inverse_name='prequisition_line_id')
    requisition_state = fields.Selection(
        [('draft', 'Draft'), ('in_progress', 'Confirmed'),
         ('open', 'Bid Selection'), ('done', 'PO Created'),
         ('cancel', 'Cancelled')],
        string='Requisition state', related='requisition_id.state')
