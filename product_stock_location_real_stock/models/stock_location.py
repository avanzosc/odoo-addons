# Copyright 2024 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class StockLocation(models.Model):
    _inherit = "stock.location"

    real_stock_location = fields.Boolean(
        string="Real Stock Location", default=False, copy=True
    )
