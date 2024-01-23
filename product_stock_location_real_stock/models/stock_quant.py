# Copyright 2024 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields


class StockQuant(models.Model):
    _inherit = "stock.quant"

    real_stock_location = fields.Boolean(
        string="Real Stock Location", store=True, copy=False,
        related="location_id.real_stock_location",
    )
