# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class StockRule(models.Model):
    _inherit = "stock.rule"

    def _get_stock_move_values(
        self,
        product_id,
        product_qty,
        product_uom,
        location_dest_id,
        name,
        origin,
        company_id,
        values,
    ):
        move_values = super()._get_stock_move_values(
            product_id,
            product_qty,
            product_uom,
            location_dest_id,
            name,
            origin,
            company_id,
            values,
        )
        sale_line = self.env["sale.order.line"].browse(values.get("sale_line_id"))
        if sale_line.exists():
            move_values.update(
                {
                    "deca_weight": sale_line.deca_weight,
                    "place_of_loading_id": sale_line.place_of_loading_id.id,
                    "place_of_delivery_id": sale_line.place_of_delivery_id.id,
                    "upload_date": sale_line.upload_date,
                }
            )
        return move_values
