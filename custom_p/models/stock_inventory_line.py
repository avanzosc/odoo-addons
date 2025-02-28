# Copyright 2025 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class StockInventoryLine(models.Model):
    _inherit = "stock.inventory.line"

    container = fields.Integer()
