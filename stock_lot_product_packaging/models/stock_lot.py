# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockLot(models.Model):
    _inherit = "stock.lot"

    product_packaging_id = fields.Many2one(
        string="Product Packaging",
        comodel_name="product.packaging",
        copy=False,
    )
    packaging_units = fields.Float(
        compute="_compute_packaging_units", store=True, copy=False
    )

    @api.depends("product_packaging_id", "product_packaging_id.qty", "product_qty")
    def _compute_packaging_units(self):
        for lot in self:
            packaging_units = 0
            if (
                lot.product_packaging_id
                and lot.product_packaging_id.qty
                and lot.product_qty
            ):
                packaging_units = lot.product_qty / lot.product_packaging_id.qty
            lot.packaging_units = packaging_units
