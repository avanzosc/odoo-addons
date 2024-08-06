# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class StockQuant(models.Model):
    _inherit = "stock.quant"

    def action_repair_reserved_quantity(self):
        move_obj = self.env["stock.move.line"]
        for quant in self:
            domain = [
                ("product_id", "=", quant.product_id.id),
                ("location_id", "=", quant.location_id.id),
                ("lot_id", "=", quant.lot_id.id),
                ("package_id", "=", quant.package_id.id),
                ("state", "=", "assigned"),
            ]
            moves = move_obj.search(domain)
            reserved_qty = (
                sum(moves.mapped("reserved_uom_qty")) - quant.reserved_quantity
            )
            quant.sudo()._update_reserved_quantity(
                quant.product_id,
                quant.location_id,
                reserved_qty,
                lot_id=quant.lot_id,
                package_id=quant.package_id,
            )
