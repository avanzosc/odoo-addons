# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    sale_price_subtotal = fields.Float(
        string="Sale Subtotal",
        digits="Product Price",
        store=True,
        copy=False,
        compute="_compute_sale_price_subtotal",
    )

    @api.depends(
        "move_ids_without_package", "move_ids_without_package.sale_price_subtotal"
    )
    def _compute_sale_price_subtotal(self):
        for picking in self:
            sale_price_subtotal = 0
            if picking.move_ids_without_package:
                sale_price_subtotal = sum(
                    picking.move_ids_without_package.mapped("sale_price_subtotal")
                )
            picking.sale_price_subtotal = sale_price_subtotal
