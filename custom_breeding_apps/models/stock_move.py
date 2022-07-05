# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    standard_price = fields.Float(digits="Standard Cost Decimal Precision")
