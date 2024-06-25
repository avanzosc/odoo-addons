# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    show_empty_location = fields.Boolean(
        string="Show Emptying Location",
        related="picking_type_id.show_empty_location",
        store=True,
    )

    def button_empty_location(self):
        self.ensure_one()
        if self.move_line_ids:
            self.move_line_ids.unlink()
        if self.location_id:
            stock = self.env["stock.quant"].search(
                [("location_id", "=", self.location_id.id)]
            )
            for line in stock:
                if line.available_quantity > 0:
                    self.env["stock.move.line"].create(
                        {
                            "product_id": line.product_id.id,
                            "location_id": self.location_id.id,
                            "location_dest_id": self.location_dest_id.id,
                            "owner_id": line.owner_id.id,
                            "lot_id": line.lot_id.id,
                            "qty_done": line.available_quantity,
                            "product_uom_id": line.product_uom_id.id,
                            "picking_id": self.id,
                        }
                    )
