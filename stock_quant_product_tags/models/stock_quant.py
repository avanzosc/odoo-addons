# Copyright 2025 Lucía Echeverría - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class StockQuant(models.Model):
    _inherit = "stock.quant"

    product_tag_ids = fields.Many2many(
        related="product_id.product_tag_ids", string="Product Tags", readonly=True
    )
