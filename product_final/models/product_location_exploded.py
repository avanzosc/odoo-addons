# Copyright 2022 Patxi Lersundi 
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class ProductLocationExploded(models.Model):
    _name= 'product.location.exploded'
    _order="product_id, product_final_id, position asc"
    _rec_name = 'product_final_id'

    product_final_id = fields.Many2one(
        comodel_name="product.final", string="Final Product", required=True)
    position = fields.Char(string="Position")
    product_id = fields.Many2one(
        comodel_name="product.product", string="Product", required=True)
