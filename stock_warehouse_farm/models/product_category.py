# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class ProductCategory(models.Model):
    _inherit = 'product.category'

    type_id = fields.Many2one(
        string='Section',
        comodel_name='category.type')
    type_ids = fields.Many2many(
        string='Sections',
        comodel_name='category.type',
        relation="rel_productcateg_categtype",
        column1="category_type_id",
        column2="product_category_id")
