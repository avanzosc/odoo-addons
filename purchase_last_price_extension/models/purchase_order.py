# Copyright 2022 Daniel Campos - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api
import odoo.addons.decimal_precision as dp


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    standard_price = fields.Float(
        string='Cost Price',
        related='product_id.standard_price', readonly=True)
    standard_price_subtotal = fields.Float(
        string='Cost Price Subtotal',
        compute='_compute_starndar_price_subtotal',
        store=True, digits=dp.get_precision('Product Price'))
    last_purchase_price = fields.Float(
        related='product_id.last_purchase_price', readonly=True, store=True)
    last_purchase_price_subtotal = fields.Float(
        string='Last Purchase Price Subtotal',
        compute='_compute_last_price_subtotal',
        store=True, digits=dp.get_precision('Product Price'))
    product_category = fields.Many2one(
        string='Category', comodel_name='product.category',
        related='product_id.categ_id', readonly=True, store=True)

    @api.depends('standard_price', 'product_uom_qty',)
    def _compute_starndar_price_subtotal(self):
        for record in self:
            total = 0
            if record.standard_price and record.product_uom_qty:
                total = record.standard_price * record.product_uom_qty
            record.standard_price_subtotal = total

    @api.depends('last_purchase_price', 'product_uom_qty',)
    def _compute_last_price_subtotal(self):
        for record in self:
            total = 0
            if record.last_purchase_price and record.product_uom_qty:
                total = record.last_purchase_price * record.product_uom_qty
            record.last_purchase_price_subtotal = total
