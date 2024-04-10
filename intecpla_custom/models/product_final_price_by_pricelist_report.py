# Copyright 2020 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class ProductFinalPriceByPricelist(models.Model):
    _inherit = "product.final.price.by.pricelist.report"

    description_sale_es = fields.Char(
        string="Name of the product in sales (Spanish)", copy=False
    )
    description_sale_en = fields.Char(
        string="Name of the product in sales (English)", copy=False
    )
    description_sale_cat = fields.Char(
        string="Name of the product in sales (Catalan)", copy=False
    )

    _depends = {
        "product.location.exploded": [
            "product_final_id",
            "position",
            "product_id",
        ],
        "product.price.by.pricelist": [
            "product_id",
            "pricelist_id",
            "price_unit",
            "description_sale_es",
            "description_sale_en",
            "description_sale_cat",
        ],
    }

    def _select(self):
        return (
            super()._select()
            + ", product_price.description_sale_es as description_sale_es, "
            "product_price.description_sale_en as description_sale_en, "
            "product_price.description_sale_cat as description_sale_cat "
        )

    def _group_by(self):
        return (
            super()._group_by()
            + ", product_price.description_sale_es, description_sale_en,"
            " product_price.description_sale_cat"
        )
