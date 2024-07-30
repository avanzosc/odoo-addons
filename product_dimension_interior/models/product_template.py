from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    interior_length = fields.Float(string="Interior Length")
    interior_height = fields.Float(string="Interior Height")
    interior_width = fields.Float(string="Interior Width")
