# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    lineal_id = fields.Many2one(
        string='Lineal',
        comodel_name='product.lineal',
        related='product_id.lineal_id',
        store=True)
