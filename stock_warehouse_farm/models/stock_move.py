# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class StockMove(models.Model):
    _inherit = 'stock.move'

    category_type_id = fields.Many2one(
        string='Category Type',
        comodel_name='category.type',
        related='picking_id.category_type_id',
        store=True)
