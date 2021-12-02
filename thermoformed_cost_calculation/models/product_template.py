# Copyright 2021 Berezi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    density = fields.Float(
        string='Density')
