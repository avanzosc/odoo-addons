# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockInventoryLine(models.Model):
    _inherit = "stock.inventory.line"

    casualty_qty = fields.Float(string="Casualties")

    @api.onchange("casualty_qty")
    def onchange_casualty_qty(self):
        self.ensure_one()
        if self.casualty_qty:
            self.product_qty = self.theoretical_qty - self.casualty_qty
