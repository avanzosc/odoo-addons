# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models
from odoo.tools.float_utils import float_is_zero


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
                ("owner_id", "=", quant.owner_id.id),
                ("state", "=", "assigned"),
            ]
            moves = move_obj.search(domain)
            reserved_qty = (
                sum(moves.mapped("quantity_product_uom")) - quant.reserved_quantity
            )
            if float_is_zero(
                reserved_qty, precision_rounding=quant.product_id.uom_id.rounding
            ):
                continue
            quant.sudo()._update_reserved_quantity(
                quant.product_id,
                quant.location_id,
                reserved_qty,
                lot_id=quant.lot_id,
                package_id=quant.package_id,
                owner_id=quant.owner_id,
            )
