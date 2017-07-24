# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, api


class ProductTemplate(models.Model):

    _inherit = 'product.template'

    @api.multi
    def _compute_count_orderpoints(self):
        orderpoint_model = self.env['stock.warehouse.orderpoint']
        for record in self:
            domain = [('product_id', 'in', record._get_products())]
            record.count_orderpoints = orderpoint_model.search_count(domain)

    count_orderpoints = fields.Float(string="Count Orderpoints",
                                     compute="_compute_count_orderpoints")


class ProductProduct(models.Model):

    _inherit = 'product.product'

    @api.multi
    def _compute_count_orderpoints(self):
        orderpoint_model = self.env['stock.warehouse.orderpoint']
        for record in self:
            domain = [('product_id', '=', record.id)]
            record.count_orderpoints = orderpoint_model.search_count(domain)

    count_orderpoints = fields.Float(string="Count Orderpoints",
                                     compute="_compute_count_orderpoints")
