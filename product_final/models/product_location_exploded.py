# Copyright 2022 Patxi Lersundi
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class ProductLocationExploded(models.Model):
    _name = "product.location.exploded"
    _order = "product_id, product_final_id, position asc"
    _rec_name = "product_final_id"

    product_final_id = fields.Many2one(
        comodel_name="product.final", string="Final Product", required=True, copy=False
    )
    position = fields.Char()
    product_id = fields.Many2one(
        comodel_name="product.product",
        string="Product",
        required=True,
    )
    view_version_id = fields.Many2one(
        string="View version", comodel_name="product.final.view.version", copy=False
    )
    product_list_version_id = fields.Many2one(
        string="Product List Version",
        comodel_name="product.final.product.list.version",
        copy=False,
    )
    initial_sn = fields.Text(string="Initial S/N", copy=False)
    final_sn = fields.Text(string="Final S/N", copy=False)
    observations = fields.Text(copy=False)
    internal_note = fields.Text(copy=False)
    alternative_sales_code = fields.Char(
        string="Alternative sales code",
        related="product_id.alternative_sales_code",
        store=True,
    )
    description_sale_es = fields.Char(
        string="Name of the product in sales (Spanish)",
        related="product_id.description_sale_es",
        store=True,
    )
    description_sale_en = fields.Char(
        string="Name of the product in sales (English)",
        related="product_id.description_sale_en",
        store=True,
    )
    description_sale_cat = fields.Char(
        string="Name of the product in sales (Catalan)",
        related="product_id.description_sale_cat",
        store=True,
    )
    active = fields.Boolean(default=True)
