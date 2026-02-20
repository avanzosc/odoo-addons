# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def button_validate(self):
        for picking in self:
            lines_to_remove = picking.move_line_ids.filtered(
                lambda line: line.qty_done == 0 and line.state not in ("done", "cancel")
            )
            if lines_to_remove:
                lines_to_remove.unlink()
        return super().button_validate()
