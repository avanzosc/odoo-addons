# Copyright 2025 Ane Gurruchaga - AvanzOSC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, models
from odoo.exceptions import ValidationError


class ProductPricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    def _get_discounted_price(self, price, discount, positive=False):
        if positive:
            return price / ((100 - discount) / 100)
        return price * ((100 - discount) / 100)

    def apply_discount(self, discount, positive=False, price_fields=None):
        if discount and discount <= 0.0:
            raise ValidationError(_("Discount must be greater than 0.0"))
        for record in self:
            values = {}
            for price_field in price_fields:
                values[price_field] = record._get_discounted_price(
                    record[price_field], discount, positive=positive
                )
            record.write(values)
