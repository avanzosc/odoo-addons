# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    product_brand_code = fields.Char(
        related="purchase_line_id.product_brand_code",
        store=True,
    )
    product_brand_id = fields.Many2one(
        comodel_name="product.brand",
        related="purchase_line_id.product_brand_id",
        store=True,
    )
