# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    sale_price_unit = fields.Float(
        string="Sale Unit Price",
        digits="Product Price",
        related="move_id.sale_price_unit",
        store=True,
        copy=False,
    )
