# Copyright 2021 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProductPackaging(models.Model):
    _inherit = 'product.packaging'

    packaging_length = fields.Float(string='Pack Length')
    width = fields.Float(string='Pack Width')
    height = fields.Float(string='Pack Height')
