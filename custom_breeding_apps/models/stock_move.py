# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    standard_price = fields.Float(digits="Standard Cost Decimal Precision")
    date = fields.Datetime(string="Date")

    def _action_done(self, cancel_backorder=False):
        res = super()._action_done(cancel_backorder)
        for move in self:
            if (
                move.location_id.usage == "inventory"
                or move.location_dest_id.usage == "inventory"
            ) and not move.inventory_id:
                for line in move.move_line_ids:
                    if line.lot_id:
                        line.standard_price = line.lot_id.average_price
                    else:
                        line.standard_price = line.product_id.standard_price or 0.0
        return res
