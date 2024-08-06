# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProductMaterial(models.Model):
    _name = "product.material"
    _description = "Product Material"
    _order = "name"

    name = fields.Char(string="Description")
    density = fields.Float(default=1, copy=False)
