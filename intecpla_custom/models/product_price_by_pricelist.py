# Copyright 2022 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class ProductPriceByPricelist(models.Model):
    _inherit = "product.price.by.pricelist"

    description_sale_es = fields.Char(
        string="Name of the product in sales (Spanish)",
        copy=False,
        store=True,
        related="product_id.description_sale_es",
    )
    description_sale_en = fields.Char(
        string="Name of the product in sales (English)",
        copy=False,
        store=True,
        related="product_id.description_sale_en",
    )
    description_sale_cat = fields.Char(
        string="Name of the product in sales (Catalan)",
        copy=False,
        store=True,
        related="product_id.description_sale_cat",
    )
