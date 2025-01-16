# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    def write(self, vals):
        result = super().write(vals)
        if "qty_done" in vals:
            self._put_last_move_locations_in_lots()
        return result

    def _put_last_move_locations_in_lots(self):
        for line in self.filtered(lambda x: x.move_id.state == "done" and x.lot_id):
            last_move_locations = ("%s - %s") % (
                line.location_id.name,
                line.location_dest_id.name,
            )
            line.lot_id.last_move_locations = last_move_locations
