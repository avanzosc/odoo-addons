# Copyright 2018 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    product_shipping_length = fields.Float(
        "Length", related="product_id.shipping_length", store=True
    )
