# Copyright (c) 2018 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    property_product_pricelist_id = fields.Many2one(
        comodel_name='product.pricelist', string='Pricelist')
