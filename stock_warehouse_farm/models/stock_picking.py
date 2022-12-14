# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    category_type_id = fields.Many2one(
        string='Origin Section',
        comodel_name='category.type',
        related='picking_type_id.category_type_id',
        store=True)
    dest_category_type_id = fields.Many2one(
        string='Destination Section',
        comodel_name='category.type',
        related='picking_type_id.dest_category_type_id',
        store=True)
