# Copyright 2025 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockLot(models.Model):
    _inherit = "stock.lot"

    lot_value = fields.Float(
        digits="Account",
        store=True,
        compute="_compute_lot_value",
        help=("Lot quantity multiplied by the lot cost."),
    )

    @api.depends("product_qty", "purchase_price")
    def _compute_lot_value(self):
        for lot in self:
            lot.lot_value = lot.product_qty * lot.purchase_price

    @api.model
    def recompute_lot_values(self):
        self._compute_lot_value()
