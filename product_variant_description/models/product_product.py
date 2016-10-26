# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    variant_description = fields.Char(string='Description', translate=True)
    html_variant_description = fields.Html(
        string='HTML description', translate=True)
