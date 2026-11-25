# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    lineage_id = fields.Many2one(
        string="Lineage",
        comodel_name="lineage",
        related="lot_id.lineage_id",
        store=True,
    )
    product_category_id = fields.Many2one(
        string="Product Category",
        comodel_name="product.category",
        related="product_id.categ_id",
        store=True,
    )
