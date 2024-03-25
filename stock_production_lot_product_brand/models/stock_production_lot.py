# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockProductionLot(models.Model):
    _inherit = "stock.production.lot"

    product_brand_id = fields.Many2one(
        string="Product brand",
        comodel_name="product.brand",
        related="product_id.product_brand_id",
        store=True,
        copy=False,
    )
