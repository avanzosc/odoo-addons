# -*- coding: utf-8 -*-
# Copyright 2016 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    customer_ids = fields.One2many(
        comodel_name='product.supplierinfo', inverse_name='product_id',
        string='Customer', domain=[('type', '=', 'customer')])
    supplier_ids = fields.One2many(
        comodel_name='product.supplierinfo', inverse_name='product_id',
        string='Supplier', domain=[('type', '=', 'supplier')])
