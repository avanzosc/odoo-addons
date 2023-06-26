# Copyright 2022 Patxi Lersundi
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class ProductLocationExploded(models.Model):
    _name = "product.location.exploded"
    _description = "Products Exploded Location"
    _order = "product_final_id, position asc"
    _rec_name = "product_final_id"

    product_final_id = fields.Many2one(
        comodel_name="product.final", string="Final Product", required=True
    )
    position = fields.Char(string="Position")
    product_id = fields.Many2one(
        comodel_name="product.product", string="Product", required=True
    )
    comments = fields.Text(string="Comments")

    _sql_constraints = [
        ("location_exploded_uniq", "unique (product_final_id, position, product_id)",
         "The combination of final product, product and position must be unique !"),
    ]

