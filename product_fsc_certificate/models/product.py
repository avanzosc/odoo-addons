
from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_fsc_certificate = fields.Boolean('Is FSC certificate')


class ProductProduct(models.Model):
    _inherit = "product.product"

    is_fsc_certificate = fields.Boolean('Is FSC certificate', related="product_tmpl_id.is_fsc_certificate")
