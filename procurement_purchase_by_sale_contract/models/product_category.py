# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from openerp import models, fields


class ProductCategory(models.Model):
    _inherit = 'product.category'

    procured_purchase_grouping = fields.Selection(
        selection_add=[('sale_contract', 'Group by sale contract')])
