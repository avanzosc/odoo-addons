# Copyright 2023 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models



class ProductSupplierinfo(models.Model):
    _inherit = "product.supplierinfo"
    _order = "sequence, min_qty desc, price_with_discount"

    price_with_discount = fields.Float(
        string="Price with discount",
        store=True,
        copy=False,
        compute="_compute_price_without_discount",
        digits="Product Price",
    )

    @api.depends("price", "discount")
    def _compute_price_without_discount(self):
        for info in self:
            price = info.price
            if info.discount:
                price = info.price - ((info.price * info.discount) / 100)
            info.price_with_discount = price
