
from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    fsc_certificate = fields.Boolean('FSC certificate')


class ProductProduct(models.Model):
    _inherit = "product.product"

    fsc_certificate = fields.Boolean('FSC certificate', related="product_tmpl_id.fsc_certificate")
