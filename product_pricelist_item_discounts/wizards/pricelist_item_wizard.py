# Copyright 2023 Leire Martinez de Santos - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class CreateProductPricelistItemDiscounts(models.TransientModel):
    _name = "create.pricelist_item.discount"
    _description = "Wizard to apply pricelist item discounts"

    discount = fields.Float(string="Discount", required=True)
    confirm_text = fields.Char('Confirm Text')
    positive = fields.Boolean('Positive', help="Apply increment on price")
    price = fields.Boolean(string="Price", default=True)
    pvp = fields.Boolean(string="PVP")

    def _get_discount_price_fields(self):
        self.ensure_one()
        return [
            (self.price, "fixed_price"),
            (self.pvp, "pvp_price"),
        ]

    @api.multi
    def button_apply_discounts(self):
        self.ensure_one()
        selected_ids = self.env.context.get('active_ids', [])
        price_fields = [
            price_field
            for apply_discount, price_field in self._get_discount_price_fields()
            if apply_discount
        ]
        item_ids = self.env['product.pricelist.item'].browse(selected_ids)
        item_ids.apply_discount(
            self.discount, positive=self.positive, price_fields=price_fields)
