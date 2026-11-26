# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProductClass(models.Model):
    _name = "product.class"
    _description = "Product class"

    name = fields.Char(string="Product class", required=True, copy=False)
