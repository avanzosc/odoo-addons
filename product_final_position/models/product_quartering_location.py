# Copyright 2022 AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductQuarteringLocation(models.Model):
    _name = "product.quartering.location"
    _description = "Product Quartering Locations"
    _order = "product_final_id,position"

    product_final_id = fields.Many2one(
        comodel_name="product.final",
        string="Final Product",
    )
    product_id = fields.Many2one(
        comodel_name="product.product",
        string="Product",
    )
    position = fields.Char(string="Position")
