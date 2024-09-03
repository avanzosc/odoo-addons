# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class ProductCategory(models.Model):
    _inherit = "product.category"

    name = fields.Char(translate=True)
