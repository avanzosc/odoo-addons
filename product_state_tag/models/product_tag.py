# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class ProductTag(models.Model):
    _name = 'product.tag'
    _description = "Product tags"

    name = fields.Char(string='Description', required=True)
