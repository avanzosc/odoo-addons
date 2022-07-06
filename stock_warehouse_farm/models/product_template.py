# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    category_type_id = fields.Many2one(
        string='Section',
        comodel_name='category.type',
        related='categ_id.type_id',
        store=True)
    type_ids = fields.Many2many(
        string='Sections',
        comodel_name='category.type',
        relation="rel_product_categtype",
        column1="product_id",
        column2="product_category_id",
        related="categ_id.type_ids",
        store=True)
