
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductPricelistItem(models.Model):
    _inherit = 'product.pricelist.item'

    def open_discount_wizard(self):
        action = self.env.ref('product_pricelist_item_discount.action_pricelist_apply_discount')
        action['views'] = [(None, 'form')]
        action['res_id'] = self.id
        return action

    def apply_discount(self, discount):
        if discount and discount <= 0.0:
            raise ValidationError(_('Discount must be greater than 0.0'))
        for record in self:
            record.fixed_price = record.fixed_price - (record.fixed_price * discount / 100)
