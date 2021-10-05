
from odoo import models


class Website(models.Model):
    _inherit = 'website'

    def _get_show_pricelist_available(self):
        return self.env['product.pricelist'].search([
            ('show_price_website', '=', True)
        ])
