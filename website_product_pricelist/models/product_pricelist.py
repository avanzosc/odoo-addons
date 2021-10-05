
from odoo import fields, models


class ProductPricelist(models.Model):

    _inherit = "product.pricelist"

    show_price_website = fields.Boolean('Show Price on Website')
