# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class StockMove(models.Model):
    _inherit = "stock.move"

    @api.model
    def create(self, vals):
        if "purchase_line_id" in vals and vals.get("purchase_line_id", False):
            line = self.env["purchase.order.line"].browse(
                vals.get("purchase_line_id"))
            vals["name"] = line.name
        move = super().create(vals)
        return move
