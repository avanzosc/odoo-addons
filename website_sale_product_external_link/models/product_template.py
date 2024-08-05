from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    website_link = fields.Char(
        help="Website page. Example: http://www.example.com",
    )
