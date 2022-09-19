# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockProductionLot(models.Model):
    _inherit = "stock.production.lot"
    _order = "name desc"

    standard_price = fields.Float(
        string="Standard Price",
        compute="_compute_standard_price")

    def _compute_standard_price(self):
        for line in self:
            line.standard_price = 0
            standard_price_line = self.env["stock.move.line"].search([
                ("lot_id", "=", line.id),
                ("picking_code", "=", "incoming"),
                ("standard_price", ">", 0)], limit=1)
            if standard_price_line:
                line.standard_price = standard_price_line.standard_price
