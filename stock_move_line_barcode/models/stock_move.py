# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class StockMove(models.Model):
    _inherit = "stock.move"

    def action_show_details(self):
        result = super(StockMove, self).action_show_details()
        if (self.product_id.tracking and
            self.product_id.tracking == "serial" and
                self.state not in ('done', 'cancel')):
            result["context"]["default_for_barcode"] = True
        return result

    def _generate_serial_move_line_commands(self, lot_names,
                                            origin_move_line=None):
        move_lines = super(
            StockMove, self)._generate_serial_move_line_commands(
                lot_names, origin_move_line=origin_move_line)
        for line in move_lines:
            if (isinstance(line[2], dict) and "lot_name" in line[2] and
                    line[2].get("lot_name", False)):
                line[2]["barcode_scanned"] = line[2].get("lot_name")
        return move_lines
