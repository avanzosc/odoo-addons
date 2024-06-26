# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class StockQuant(models.Model):
    _inherit = "stock.quant"

    product_categ_id = fields.Many2one(
        comodel_name="product.category",
        string="Category",
        related="product_id.categ_id",
        store=True,
    )
    root_category_id = fields.Many2one(
        comodel_name="product.category",
        string="Root Category",
        related="product_id.root_category_id",
        store=True,
    )
    parent_category_id = fields.Many2one(
        comodel_name="product.category",
        string="Parent Category",
        related="product_categ_id.parent_id",
        store=True,
    )
