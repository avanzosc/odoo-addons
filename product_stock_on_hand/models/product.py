# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, api
from openerp.addons import decimal_precision as dp


class ProductTemplate(models.Model):

    _inherit = 'product.template'

    @api.depends('product_variant_ids', 'product_variant_ids.quant_ids',
                 'product_variant_ids.quant_ids.qty',
                 'product_variant_ids.quant_ids.location_id',
                 'product_variant_ids.quant_ids.location_id.stock_on_hand',
                 'product_variant_ids.quant_ids.reservation_id')
    @api.multi
    def _compute_stock_on_hand(self):
        for record in self:
            record.stock_on_hand = sum(
                record.mapped('product_variant_ids.quant_ids').filtered(
                    lambda x: x.location_id.stock_on_hand and
                    not x.reservation_id).mapped('qty'))

    stock_on_hand = fields.Float(
        string="Stock On Hand", store=True, compute="_compute_stock_on_hand",
        digits=dp.get_precision('Product Unit of Measure'))


class ProductProduct(models.Model):

    _inherit = 'product.product'

    @api.depends('quant_ids', 'quant_ids.qty', 'quant_ids.location_id',
                 'quant_ids.location_id.stock_on_hand',
                 'quant_ids.reservation_id')
    @api.multi
    def _compute_stock_on_hand(self):
        for record in self:
            record.stock_on_hand = sum(
                record.quant_ids.filtered(
                    lambda x: x.location_id.stock_on_hand and
                    not x.reservation_id).mapped('qty'))

    stock_on_hand = fields.Float(
        string="Stock On Hand", store=True, compute="_compute_stock_on_hand",
        digits=dp.get_precision('Product Unit of Measure'))
    quant_ids = fields.One2many(comodel_name='stock.quant',
                                inverse_name='product_id', string='Quants')
