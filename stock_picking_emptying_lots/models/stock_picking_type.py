# Copyright 2025 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockPickingType(models.Model):
    _inherit = "stock.picking.type"

    emptying_type = fields.Boolean(string="Emptying Lots Type", default=False)
