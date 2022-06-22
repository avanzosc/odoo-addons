# Copyright 2022 AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    quartering_location_ids = fields.One2many(
        comodel_name="product.quartering.location",
        inverse_name="product_id",
        string="Quartering Location",
    )
