# Copyright 2020 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    categ_id = fields.Many2one(
        comodel_name="product.category",
        compute="_compute_categ_id",
        compute_sudo=True,
        store=True,
    )
    product_brand_id = fields.Many2one(
        comodel_name="product.brand",
        compute="_compute_product_brand_id",
        store=True,
    )

    @api.depends("product_id.categ_id")
    def _compute_categ_id(self):
        for move in self:
            move.categ_id = move.product_id.categ_id

    @api.depends("product_id.product_brand_id")
    def _compute_product_brand_id(self):
        for move in self:
            move.product_brand_id = move.product_id.product_brand_id
