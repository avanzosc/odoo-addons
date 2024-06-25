# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductPricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    product_pricelist_price = fields.Float(
        string="Pricelist Price", compute="_compute_product_pricelist_price"
    )

    def _compute_product_pricelist_price(self):
        for item in self:
            if item.product_id and item.pricelist_id:
                price = item.product_id.with_context(
                    pricelist=item.pricelist_id.id, date=fields.Date.today()
                ).price
            elif item.product_tmpl_id and item.pricelist_id:
                price = item.product_tmpl_id.with_context(
                    pricelist=item.pricelist_id.id, date=fields.Date.today()
                ).price
            else:
                price = 0
            item.product_pricelist_price = price
