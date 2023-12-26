# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def button_force_done_detailed_operations(self):
        result = super().button_force_done_detailed_operations()
        for line in self.move_line_ids_without_package:
            line._onchange_product_id()
            line.onchange_standard_price()
        return result
