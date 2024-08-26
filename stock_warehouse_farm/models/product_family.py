# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProductFamily(models.Model):
    _name = "product.family"
    _description = "Product Family"

    name = fields.Char(string="Name")
