# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    product_categ_type_id = fields.Many2one(
        string='Product Category Type',
        comodel_name='category.type',
        related='product_id.categ_id.type_id',
        store=True)
