# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    categ_id = fields.Many2one(
        string='Product Category',
        comodel_name='product.category',
        related='product_id.categ_id',
        store=True)
    category_type_id = fields.Many2one(
        string='Section',
        comodel_name='category.type',
        related='categ_id.type_id',
        store=True)
