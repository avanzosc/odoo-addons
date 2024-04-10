# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    def _default_lot_name(self):
        lot_name = ""
        if (
            "show_lots_text" in self.env.context
            and self.env.context.get("show_lots_text", False)
            and "default_picking_id" in self.env.context
            and self.env.context.get("default_picking_id", False)
            and "default_product_id" in self.env.context
            and self.env.context.get("default_product_id", False)
        ):
            picking = self.env["stock.picking"].browse(
                self.env.context.get("default_picking_id")
            )
            if (
                picking
                and picking.picking_type_id
                and picking.picking_type_id.code == "incoming"
            ):
                product = self.env["product.product"].browse(
                    self.env.context.get("default_product_id")
                )
                if product.categ_id and product.categ_id.sequence_id:
                    lot_name = product.categ_id.sequence_id.next_by_id()
                else:
                    lot_name = self.env.ref(
                        "stock.sequence_production_lots"
                    ).next_by_id()
        return lot_name

    lot_name = fields.Char(default=_default_lot_name)
