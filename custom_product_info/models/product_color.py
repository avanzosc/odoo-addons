# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductColor(models.Model):
    _name = "product.color"
    _description = "Product Color"

    name = fields.Char(
        string="Name"
    )
