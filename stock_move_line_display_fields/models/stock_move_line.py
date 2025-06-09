# Copyright 2025 Lucía Echeverría- AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    purchase_cost = fields.Float(
        related="lot_id.purchase_cost",
        string="Purchase Cost",
        readonly=True,
        store=False,
    )
