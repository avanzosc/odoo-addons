# Copyright 2021 Berezi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class ProductPackaging(models.Model):
    _inherit = 'product.packaging'

    height = fields.Float("Height")
    width = fields.Float("Width")
    packaging_length = fields.Float("Length")
