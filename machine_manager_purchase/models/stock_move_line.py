# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    def create_machine(self):
        for line in self:
            vals = line._catch_values_to_create_machine()
            self.env["machine"].create(vals)

    def _catch_values_to_create_machine(self):
        name = ""
        if self.move_id.purchase_line_id:
            name = self.move_id.purchase_line_id.order_id.name
        if self.product_id.default_code:
            name = (
                self.product_id.default_code
                if not name
                else "{} {}".format(name, self.product_id.default_code)
            )
        if self.lot_name:
            name = self.lot_name if not name else "{} {}".format(name, self.lot_name)
        vals = {
            "name": name,
            "product_id": self.product_id.id,
            "move_line_id": self.id,
        }
        if self.lot_id:
            vals["serial_id"] = self.lot_id.id
        return vals
