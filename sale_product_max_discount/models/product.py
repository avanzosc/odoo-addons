# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, api


class ProductProduct(models.Model):

    _inherit = 'product.product'

    @api.multi
    @api.depends('lst_price', 'standard_price', 'min_margin')
    def _compute_max_discount(self):
        for record in self.filtered(lambda x: x.lst_price):
            max_discount = round((
                ((record.lst_price - record.standard_price) -
                 (record.min_margin / 100 * record.lst_price)) /
                record.lst_price * 100), 2)
            record.max_discount = max(max_discount, 0.0)

    max_discount = fields.Float(string='Max Discount', store=True,
                                compute='_compute_max_discount')
