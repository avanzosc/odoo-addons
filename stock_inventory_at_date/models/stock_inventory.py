# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockInventory(models.Model):
    _inherit = "stock.inventory"

    accounting_date = fields.Date(string="Date", default=fields.Date.today())

    def action_open_inventory_lines(self):
        result = super().action_open_inventory_lines()
        result["context"].update({"inventory_date": self.accounting_date})
        return result

    def action_validate(self):
        result = super().action_validate()
        if self.accounting_date:
            for move in self.move_ids:
                move.date = self.accounting_date
                for line in move.move_line_ids:
                    line.date = self.accounting_date
        return result
