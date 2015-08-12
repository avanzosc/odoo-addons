# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from openerp import models, fields


class StockPlanning(models.Model):
    _inherit = 'stock.planning'

    product_type = fields.Many2one(
        'product.product.type', 'Product Type', store=True, translate=True,
        related='product.product_tmpl_id.product_type'
        )
