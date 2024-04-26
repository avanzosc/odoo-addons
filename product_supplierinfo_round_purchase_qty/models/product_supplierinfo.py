# Copyright 2020 Alfredo de la Fuente - Avanzosc S.L.
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class ProductSupplierinfo(models.Model):
    _inherit = "product.supplierinfo"

    round_quantity_purchase = fields.Float(
        string="Round quantity purchase",
        digits="Product Unit of Measure",
        default=0.0,
        copy=False,
    )
