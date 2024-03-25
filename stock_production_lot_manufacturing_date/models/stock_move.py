# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class StockMove(models.Model):
    _inherit = "stock.move"

    def write(self, vals):
        result = super().write(vals)
        if "state" in vals and vals.get("state") == "done":
            moves = self.filtered(lambda x: x.production_id)
            if moves:
                moves.put_manufacturing_date_in_lot()
        return result

    def put_manufacturing_date_in_lot(self):
        for move in self:
            if move.move_line_ids:
                lines = move.move_line_ids.filtered(lambda x: x.lot_id)
                for line in lines:
                    line.lot_id.manufacturing_date = move.date
