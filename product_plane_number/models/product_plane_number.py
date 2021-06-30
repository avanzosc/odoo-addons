# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields


class ProductPlaneNumber(models.Model):
    _name = 'product.plane.number'
    _description= 'Plane number'

    name = fields.Char(
        string='Plane number', required=True)
