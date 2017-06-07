# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, api


class StockLabelReportData(models.Model):

    _name = 'stock.label.report.data'

    @api.multi
    @api.depends('product_qty', 'ul_id', 'ul_id.qty')
    def _compute_ul_qty(self):
        for record in self.filtered(lambda x: x.ul_id.qty):
            to_sum = (record.product_qty % record.ul_id.qty) and 1 or 0
            record.ul_computed_qty = int((record.product_qty /
                                          record.ul_id.qty)) + to_sum

    picking_id = fields.Many2one(comodel_name='stock.picking',
                                 string='Picking')
    product_id = fields.Many2one(comodel_name='product.product',
                                 string='Product')
    product_qty = fields.Float(string='Product Quantity')
    ul_id = fields.Many2one(comodel_name='product.ul', string='Package type')
    ul_qty = fields.Integer(string='Package Quantity')
    lot_id = fields.Many2one(comodel_name='stock.production.lot', string='Lot')
    ul_computed_qty = fields.Integer(string='Computed Package Qty',
                                     compute='_compute_ul_qty', store=True)
