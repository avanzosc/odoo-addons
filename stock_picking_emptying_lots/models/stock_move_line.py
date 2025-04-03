# Copyright 2025 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    def create_emptying_lots_movelines(self, line, picking):
        if line and picking:
            if (
                picking
                and line.product_id.tracking != "none"
                and line.product_id.categ_id.emptying_type
            ):
                qty = line.product_id.with_context(
                    location_qty_available=True, location=line.location_id.id
                )._compute_quantities_dict(
                    line.lot_id.id,
                    line.owner_id.id,
                    line.package_id.id,
                )[
                    line.product_id.id
                ][
                    "qty_available"
                ]
                if qty > 0:
                    move_line = self.env["stock.move.line"].create(
                        {
                            "picking_id": picking.id,
                            "product_id": line.product_id.id,
                            "product_uom_id": line.product_id.uom_id.id,
                            "qty_done": qty,
                            "location_id": line.location_id.id,
                            "location_dest_id": picking.location_dest_id.id,
                            "lot_id": line.lot_id.id,
                        }
                    )
                    move_line.move_id.product_uom_qty = qty
