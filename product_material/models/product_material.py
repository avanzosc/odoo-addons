# Copyright 2021 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class ProductMaterial(models.Model):
    _name = "product.material"
    _description = "Product Material"

    name = fields.Char(string='Name')
