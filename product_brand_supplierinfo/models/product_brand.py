# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class ProductBrand(models.Model):
    _inherit = "product.brand"

    code = fields.Char(string="Brand Code", copy=False)
    marking = fields.Char(copy=False)
