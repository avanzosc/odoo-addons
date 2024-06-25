# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    container = fields.Float(
        string="Quantity contained per package",
        related="product_packaging.qty",
        store=True,
        copy=False,
    )
