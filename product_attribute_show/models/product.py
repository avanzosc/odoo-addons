
from odoo import api, fields, models


class ProductAttribute(models.Model):
    _inherit = "product.attribute"

    attr_display = fields.Boolean('Display attribute', default=True)


class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"

    attr_display = fields.Boolean('Display attribute value', default=True)
