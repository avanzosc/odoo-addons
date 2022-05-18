# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class ProductLineal(models.Model):
    _name = 'product.lineal'
    _description = 'Lineal Product'

    name = fields.Char(string='Lineal')
