# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockQuant(models.Model):
    _inherit = "stock.quant"

    lot_product_id = fields.Many2one(
        string="Lot Product",
        comodel_name="product.product",
        related="lot_id.product_id",
        store=True,
        copy=False,
    )
    lot_create_date = fields.Datetime(
        string="lot Creation Date", related="lot_id.create_date", store=True, copy=False
    )
    different_products = fields.Boolean(
        compute="_compute_different_products", store=True, copy=False
    )

    @api.depends("product_id", "lot_product_id")
    def _compute_different_products(self):
        for quant in self:
            quant.different_products = (
                bool(quant.lot_product_id) and quant.product_id != quant.lot_product_id
            )
