# Copyright 2025 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockOrderpoint(models.Model):
    _inherit = "stock.warehouse.orderpoint"

    qty_to_order = fields.Float(compute=False)
