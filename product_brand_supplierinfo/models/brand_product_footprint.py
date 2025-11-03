# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class BrandProductFootprint(models.Model):
    _name = "brand.product.footprint"
    _description = "Brand Products Footprint"

    name = fields.Char(string="Description", required=True, copy=False)
