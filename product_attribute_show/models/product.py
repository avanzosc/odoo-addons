
from odoo import api, fields, models


class ProductAttribute(models.Model):
    _inherit = "product.attribute"

    attr_display = fields.Boolean('Display attribute', default=True)


class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"

    attr_display = fields.Boolean('Display attribute value', default=True)


class ProductProduct(models.Model):
    _inherit = "product.product"

    def _compute_display_name(self):
        super()._compute_display_name()
        for record in self.filtered(lambda s: s.attribute_value_ids):
            display_name = record.display_name.split('(')[0]
            record.display_name = display_name

    def get_product_multiline_description_sale(self):
        res = super().get_product_multiline_description_sale()
        name = self.display_name.split('(')[0]
        if self.description_sale:
            name += '\n' + self.description_sale
        return name
