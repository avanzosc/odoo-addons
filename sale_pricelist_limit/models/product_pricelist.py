# Copyright (c) 2018 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductPricelist(models.Model):
    _inherit = 'product.pricelist'

    has_limit = fields.Boolean(string='Limited')
    limit_amount = fields.Float(string='Amount Limit')
