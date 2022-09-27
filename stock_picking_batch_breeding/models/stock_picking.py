# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def write(self, values):
        result = super(StockPicking, self).write(values)
        if "date_done" in values:
            self.batch_id.state = "draft"
            self.is_locked = False
        return result

    def button_validate(self):
        self.ensure_one()
        result = super(StockPicking, self).button_validate()
        chick = self.move_line_ids_without_package.filtered("product_id.one_day_chicken")
        if self.batch_id and self.batch_id.batch_type == "breeding" and chick:
            self.batch_id.action_load_growth_rates()
        for line in self.move_line_ids_without_package:
            line.onchange_standard_price()
        return result
