# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def write(self, values):
        result = super().write(values)
        if "date_done" in values:
            self.batch_id.state = "draft"
            self.is_locked = False
        return result

    def button_validate(self):
        result = super().button_validate()
        chick = self.move_line_ids_without_package.filtered(
            "product_id.one_day_chicken"
        )
        for picking in self:
            if picking.batch_id and picking.batch_id.batch_type == "breeding" and chick:
                picking.batch_id.action_load_growth_rates()
            for line in picking.move_line_ids_without_package:
                line.onchange_standard_price()
        return result

    def action_cancel(self):
        for picking in self:
            for line in picking.move_line_ids_without_package:
                line.qty_done = 0
        return super().action_cancel()
