# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    move_type_id = fields.Many2one(
        string="Move Type",
        comodel_name="move.type",
        related="product_id.categ_id.move_type_id",
        store=True,
    )
